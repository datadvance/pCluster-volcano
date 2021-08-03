"""
Examples of using the module pcluster, Usage
Tests
"""

from pprint import pprint
import time
import pcluster


task1 = pcluster.TaskSpec(
	name='task1-name',
	exec=["sh", "-c", "cat /logs/hello.txt"],
	env = {},
	runenv=('COBOL', 42),
	require=('NX', 2020),
	cpu=0.1,
	memory=128e6,
	storage={'NAME': '/logs'}
)

NAME_JOB = 'job'

pprint(pcluster.features(pcluster.RUNENVS))

for i in range(10):
	job = pcluster.JobSpec(
		name=NAME_JOB + str(i),
		tasks=[task1],
		owner=42
	)
	response = pcluster.submit_job(job)
	print('Job successful created with name: %s' % response['metadata']['name'])

completed = 0

time.sleep(1)
begin = time.time()

for i in range(10):
	while pcluster.status_job(NAME_JOB+str(i)) != pcluster.TaskState.COMPLETED:
		if time.time() - begin > 1000:
			break
		time.sleep(1)
	else:
		completed += 1
		print('%s%d is Completed' % (NAME_JOB, i))

assert completed == 10, "Not all jobs completed"


# # CREATE JOB
# response = submit_job(job_spec_to_dict(job1), custom_object_api)
# print('Job successful created with uid: %s' % response['metadata']['uid'])

# # SLEEP
# print('Sleeping 2 second ...')
# time.sleep(2)


# # GET POD NAMES
# pod_name_task1 = get_pod_name_by_task_name('task1-name', core_api)
# pod_name_task2 = get_pod_name_by_task_name('task2-name', core_api)


# # SLEEP
# print('Sleeping 6 second ...')
# time.sleep(6)


# # GET STATUS JOB, TASKS
# print('Status job: %s' % status_job(NAME_JOB, custom_object_api))
# print('Status task1: %s' % status_task(pod_name_task1, core_api))
# print('Status task2: %s' % status_task(pod_name_task2, core_api))
# print('-' * 20)


# # SLEEP
# print('Sleeping 3 second ...')
# time.sleep(3)


# # GET STATUS JOB, TASKS
# print('Status job: %s' % status_job(NAME_JOB, custom_object_api))
# print('Status task1: %s' % status_task(pod_name_task1, core_api))
# print('Status task2: %s' % status_task(pod_name_task2, core_api))
# print('-' * 20)


# # SLEEP
# print('Sleeping 5 second ...')
# time.sleep(5)


# # GET STATUS JOB
# print('Status job: %s' % status_job(NAME_JOB, custom_object_api))
# print('Status task1: %s' % status_task(pod_name_task1, core_api))
# print('Status task2: %s' % status_task(pod_name_task2, core_api))
# print('-' * 20)


# # SLEEP
# print('Sleeping 3 second ...\n')
# time.sleep(3)


# OUTPUT TASKs
print('stdout task1:\n%s' % pcluster.get_stdout_task('task1-name', 'job0'))
print('stdout task2:\n%s' % pcluster.get_stdout_task('task1-name', 'job1'))



# response = delete_job('job-name', custom_object_api)
# print('Job deleted with status: %s' % response['status'])
