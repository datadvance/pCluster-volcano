# Интерфейс pCluster

Требования к собственным образам:
- Переменные окружения, соответствующие установленными окружениям
  выполнения. Например: `DA__P7__RUNENV__COBOL__ACTIVATE`.
- Разработчик образа несёт ответственность за то, чтобы обеспечить
  работоспособность задач от любого пользователя в диапазоне
  идентификаторов 20000-29999 (см. `values.yaml`). Например при запуске
  задачи пользователя `owner=42` через Kubernetes в пода будет
  установлено следующее:
  ```yaml
  pod.securityContext: {runAsGroup: user2xxxx, runAsUser: user20042, runAsNonRoot: true}
  pod.container.securityContext: {allowPrivilegeEscalation: false}
  ```
  Добиться этого можно, например, путём создания 9999 пользователей
  user20001-user29999, или какими-то еще путями, `ENV HOME=/tmp/home`.
- Если образ предоставляет несколько фич (features) и/или несколько
  окружений выполнения (runenvs), то этому образу должно быть выставлено
  необходимое количество Docker-тэгов. Пример: образ с PYTHON2 и PYTHON3
  должен иметь следующие Docker-тэги: `pseven-calc-python2-13` и
  `pseven-calc-python3-42`.

Непонятные вопросы:
- ⚠️ Компаньон должен быть переписан на Go, чтобы его можно было
  скопировать внутрь пользовательского образа и запустить через него
  блок. Пока Компаньон не переписан - будем использовать наш базовый
  образ в котором будет нужный нам Python (НЕ RUNENV).

- Тот, кто готовит вычислительный ресурс (Docker-образ, Windows-хост,
  HT Condor Execute ноду), отвечает за места монтирования общей файловой
  системы: USERS & APPS.

Вопросы безопасности:
- ⚠️ Нельзя монтировать `Users` и `Apps` весь в пользовательский образ -
  так злоумышленник получит доступ ко всем файлам всех пользователей.
  Выводы:
  - Нужно монтировать хомяк при запуска расчета.
  - Нужно монтировать только run-директория при запуске "приложеньки".
- Образ (image) запуска задачи не может быть любой из интернета, а
  должен быть с нашего одобренного реестра. Образы (и блоки!) могут
  публиковать только доверенные пользователи, т.е. разработчик
  Платформы, или админ развёртывания. Основная причина - образ (и блок)
  может удалить все данные из домашней директории пользователя.




## Описание задачи

```python

# Командная строка для запуска задачи. Именно тут происходит "активация"
# среды выполнения (runenv).
# Примеры:
# - sidecar.exe --runenv=(COBOL,42)
#               --exec ${DA__P7__RUNENV__COBOL__EXECUTE} my_block.cobol
# - train.bat --sample=... --model=... # активация внутри BAT-файла
#
# Запускаемой задачи доступны следующие специальные переменные
# окружения:
# - DA__P7__PCLUSTER__STORAGE__<STORAGE_KEY>: См. описание `storage`.
exec: List[str]

# Пользователь под которым запускается задача: от 1 до 9999. Есть
# однозначное правило трансляции имени пользователя в идентификатор и
# обратно: user2xxxx. Например: owner=42 -> пользователь=user20042.
# Задача запускается от имени указанного пользователя даже когда образ
# (`image`) был задан явно. Разработчик образа несёт ответственность за
# то, чтобы обеспечить работоспособность задач от любого пользователя
# в диапазоне идентификаторов 20000-29999.
owner: int

# Переменные окружения для задачи: имя:значение.
env: Dict[str, str]

# Операционная система: "Linux" или "Windows".
# Причины появления:
# - Нужно знать ОС для реализации:
#   - Nomad: Надо явно установить `task.driver` исходя из ОС.
#   - Kubernetes/Slurm/...: Надо явно как-то "костылить" Windows-задачи.
#   - HT Condor: Может работать кросс-платформенно, не обязательно.
# - Клиент pCluster явно задает платформозависимый параметр `exec`, т.е.
#   он все-равно уже "знает" ОС.
os: str

# Окружение выполнения (runenv) и необходимое свойство (require)
# вычислительного ресурса, на котором будет запущена задача (task).
# Например, если задать `runenv=("COBOL",42) & feature=("NX","2020")`,
# то pCluster запустит задачу на ресурсе где одновременно имеется
# окружение выполнения "COBOL" версии >=42 и установлен NX версии 2020.
# В зависимости от реализации это требование может быть удовлетворено
# разными путями:
# - В системах запуска на базе Docker (Kubernetes/Volcano/Nomad/...)
#   будет использован образ (image) с именем составленным из указанных
#   значений runenv & require: "pseven-calc-cobol-42-nx-2020".
# - В системах очередей (HT Condor/SLURM/...) значения runenv & require
#   будут использоваться в требованиях к хосту в описании задачи.
#
# Сценарий: Хочу запустить свой Python script там, где есть ABAQUS:
#   runenv: ("PYTHON3", 13)  <- берется из манифеста блока
#   require: ("ABAQUS", "v42")  <- выбирает пользователь в интерфейсе
runenv: Tuple[str, int]
require: Optional[Tuple[str, Optional[str]]]

# Конкретный дополнительный узел (extension node). `None` - выбирать
# автоматически исходя из полей `runenv` и `require`.
extension_node: Optional[str]

# Количество необходимых задаче CPU-ядер. Минимальное значение = 0.01,
# что HT Condor станет одним слотом.
cpu: float

# Максимальное допустимый объём памяти в байтах по превышению которого
# реализация pCluster (HT Condor/Kubernetes/Nomad/...) имеет право убить
# задачу.
memory: int

# Список путей, которые должны быть доступны задаче. Например, если
# задать такое значение:
# storage={
#     "USER": "/Users/42/",
#     "RUN": "/Apps/13/Runs/42/",
# }
# то запущенной задаче будут доступны переменные окружения с абсолютными
# путями до соответствующих папок. На практике, при запуске
# Linux-контейнеров внутри Kubernetes пути монтируются прямо в указанный
# путь:
# - DA__P7__PCLUSTER__STORAGE__USER=/Users/42/
# - DA__P7__PCLUSTER__STORAGE__RUN=/Apps/13/Runs/42/
#
# Если же задача запускается на Windows, то путь, очевидно, будет
# отличаться и, скорее всего будет сокращен до одной буквы:
# - DA__P7__PCLUSTER__STORAGE__USER=Z:\
# - DA__P7__PCLUSTER__STORAGE__USER=Y:\
#
# Указанные выше переменные определяются в генерируемом pCluster скрипте
# запуска задачи. Он же осуществляет монтирование в случае запуска на
# дополнительных Windows-узлах.
storage: Dict[str, str]


# МЫ ТУТ

# Счетные ресурсы. Есть предложение тоже определять в `Values.yaml` ибо
# это просто. Вроде бы любая реализация позволяет "прицепить" к задаче
# метаинформацию, а значит даже при перезапуске pCluster мы может узнать
# сколько ресурсов уже захвачено имеющимися задачами, а из переменных
# окружения (установленных в `Values.yaml` узнаем какие ресурсы бывают
# и сколько их всего).
borrow?
# Filenames to redirect standard output streams into.
stderr: Optional[str] = None
stdout: Optional[str] = None
# Directory to run task in. `None` runs it in a temporary directory.
cwd: Optional[str] = None
workgroup?

```


# Интерфейс pCluster

```python

# TODO: "причесать" пример.

# Информация о возможностях кластера. Нужно, чтобы в зависимости от
# известной из манифеста блока среды выполнения (runenv), ОС показать
# пользователю список доступных "фич" и дополнительных вычислительных
# узлов.
#
# Например, когда функция выдаёт следующее:
# {
#     {
#         "os": "Linux",
#         "extension_node": null,
#         "runenv": ("PYTHON3", 42),
#         "features": [
#             ("ABAQUS","v2021.05"),
#             ("EXCEL","2020"),
#         ]
#     },
#     {
#         "os": "Linux",
#         "extension_node": "mylinuxhost",
#         "runenv": ("PYTHON3", 42),
#         "features": [
#             ("ABAQUS","v2021.05"),
#             ("EXCEL","2020"),
#         ]
#     },
#     {
#         "os": "Windows",
#         "extension_node": "mywindowshost",
#         "runenv": ("PYTHON3", 42),
#         "features": [
#             ("ABAQUS","v2021.05"),
#             ("EXCEL","2020"),
#         ]
#     }
# }
#
# Для блока с `runenv=("PYTHON3",42) и require=("ABAQUS",null)` мы
# показываем примерно следующее:
#     Runenv: [PYTHON3 (v42)]  <- информационное поле, изменить нельзя
#     Require: [ABAQUS v42 (linux)]  <- выпадающий список:
#         ABAQUS v42 (linux)
#         ABAQUS v42 (linux) @mylinuxhost
#         ABAQUS v42 (windows)
#         ABAQUS v42 (windows) @mywindowshost
#
# Если реализация pCluster построена на запуске Docker-контейнеров
# (Kubernetes/Volcano/Nomad/...), то выдача функции определяется
# имеющимися Docker-образами. Чтобы pCluster как-то узнал о них, при
# развёртывании в `Values.yaml` должны быть определены переменные
# окружения `DA__P7__PCLUSTER__CALC_IMAGE__...=...` из имён которых
# которых pCluster узнает об имеющихся Docker-образах. По соглашению
# образы именуются как pseven-calc-<runenv>-<ver>-<feature>-<ver>. Если
# один образ предоставляет несколько версий, то надо сделать несколько
# Docker-тэгов (имён), ссылающихся на один и тот же образ.
pcluster.runenv_features()

```

# Фасад блока

_И в манифесте._

```yaml
# Требуемое свойство вычислительного ресурса, на выбор. Приоритет
# отдаётся первому, если ресурс с таким свойством не найден - второму и
# так далее.
required_feature: [("COBOL", "v42"), ("COBOL", "v13"), ("COBOL", null)]
# Тут пользователю в списке покажем:
#   Required feature [EXCEL 2020 v] и список альтернатив:
#   - EXCEL 2020
#   - EXCEL 2000
#   - EXCEL 97
required_feature: [("EXCEL", null)]
```