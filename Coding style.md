## Coding style guide

### Common

Follow these simple rules if there is no language-specific rules in the
sections below.

#### Line length and indentation

-   Indent with spaces. One indent - **4 spaces**.
-   Maximum line length is **88** characters (exception is URLs in
    comments).
-   For flowing long blocks of text with fewer structural restrictions
    (docstrings or comments), the line length should be limited to **72**
    characters. **This applies to all types of files**: Python,
    JavaScript, Markdown, etc.

#### Abbreviation and naming consistency

For consistency avoid abbreviations at all. The rule is simple, we do
everything to avoid ambiguity in translations between `CamelCase`,
`underscore_case` and `UPPER_CASE`.

DO:

```python
class GtapproxModel: ...
GTAPPROX_MODEL = ...
gtapprox_model =
class UrlTransform: ...
URL_TRANSFORM =
url_transform =
```

DON'T:

```python
class GTApprox: ...
# Causes `G_T_APPROX` and `g_t_approx`.
class URLTransform: ...
# Causes `U_R_L_TRANSFORM` and `u_r_l_transform`.
```

### Python

We base our coding conventions on principles explained in
[PEP8](https://www.python.org/dev/peps/pep-0008/) and on
[Google Python Style Guide](https://github.com/google/styleguide/blob/gh-pages/pyguide.md).

We agreed to use [black](https://black.readthedocs.io) as code formatter
and follow its default rules.

This chapter contains explanations about controversial issues. New items
added on demand, when question is raised.

#### Line length

-   Maximum line length is 88 characters (by default in `black`).
-   Exceptions are:
    -   Long import statements.
    -   URLs in comments.

#### Import statements

Concerning Python import statements there are a baseline and exceptions
which proves the rule. The baseline is the following - in general prefer
importing complete names with all namespaces. So by default you do
`import package.package.module` or `import package.package`.

There are remarkable exception though. There is always a motivation for
the exception. Clear and impersonal motivation.

The following imports can be considered as a well-known parts of the
Python languages itself, so we import named directly:

-   `from typing import ...`: Type annotations from the `typing`.
-   `from collection import ...`: Well-known Python collections.

These ones come from the common sense. If you think we need to add more
exceptions here - address your thought to `sd@`&`@qa`.

-   `from .myclass import MyClass`: Local declarations from the namesake
    modules. But if there are more than just one item - prefer complete
    form: `from . import myclass` if there are `myclass.MyClass` and
    `myclass.something_else`.
-   `from pprint import pprint`: Well-known standard Python function
    inside the namesake module.
-   `import numpy as np`: Widespread and well-know abbreviation.
-   `import networkx as nx`: Widespread and well-know abbreviation.

Another exception is Django URL configuration where the context is
clearly obvious - typically file is named `urls.py` and it contains only
application URL configuration. In such cases it is OK to import widely
used URL configuration related functions directly:
`from django.conf.urls import url, include`. **Do not generalize** this
rule to anything that may seem obvious from the first sight. Better
discuss with the team first - address this to `sd@`&`@qa`.

If some **RARE** cases when import is inconveniently long then it is
acceptable to use aliases. For example when file contains dozens of
`rest_framework.response.Response` you may shorten it using aliases like
this `from rest_framework.response import Response as drf_Response`.
**Never do this for consistency** only then there is a real reason for
this.

#### Assert statements

Please leave descriptions of what happened. Note that you will see this
description when assert fails, so it is good to describe the issue
itself.

Some **GOOD** example:

```python
assert os.exists(filename), f"The file '{filename}' has disappeared!"
```

DON'T (Do not use back quotes in messages.):

```python
assert os.exists(filename), f"The file `{filename}` has disappeared!"
```

#### Non-public attribute names

Use single underscore for all non-public attributes. Use double
underscore only when really necessary, e.g. to avoid name clash with
subclasses. By default, use single underscore as prefix.

Some **GOOD** example:

```python
class A(object):
    def __init__(self):
        self._some_private_field = 42

    def _some_private_method(self):
        pass
```

#### Comments (Python)

Write comments for people! Comment must give an answer to the question
"Why?". Keep it simple and follow [these guidelines](https://google.github.io/styleguide/pyguide.html?showone=Comments#Comments).

All classes, methods and functions must have descriptive docstring.

Below you will find some example just to remember you the syntax the
we use.

Some **GOOD** example of method/function comment:

```python
def fetch_bigtable_rows(big_table, keys, other_silly_variable=None):
    """Fetches rows from a Bigtable.

    Retrieves rows pertaining to the given keys from the Table instance
    represented by big_table.  Silly things may happen if
    other_silly_variable is not None.

    Args:
        big_table: An open Bigtable Table instance.
        keys: A sequence of strings representing the key of each table
            row to fetch.
        other_silly_variable: Another optional variable, that has a much
            longer name than the other args, and which does nothing.

    Returns:
        A dict mapping keys to the corresponding table row data
        fetched. Each row is represented as a tuple of strings. For
        example:

        {"Mate": ("Rigel VII", "Preparer"),
         "Zim": ("Irk", "Invader")}

        If a key from the keys argument is missing from the dictionary,
        then that row was not found in the table.

    Raises:
        IOError: An error occurred accessing the bigtable.Table object.
    """
    pass
```

Some **GOOD** example of class comment:

```python
class SampleClass(object):
    """Summary of class here.

    Longer class information....
    Longer class information....

    Attributes:
        likes_spam: A boolean indicating if we like SPAM or not.
        eggs: An integer count of the eggs we have laid.
    """

    def __init__(self, likes_spam=False):
        """Inits SampleClass with blah."""
        self.likes_spam = likes_spam
        self.eggs = 0

    def public_method(self):
        """Performs operation blah."""
```

Some **GOOD** example of a tricky code comment:

```python
# We use a weighted dictionary search to find out where i is in
# the array. We extrapolate position based on the largest num
# in the array and the array size and then do binary search to
# get the exact number.

if i & (i-1) == 0:        # true if i is a power of 2
```

Keep closing quotes on the same line for the single line comments. In
all other cases move closing quotes to a separate line.

DO:

```python
def some_function():
    """Method description is short and descriptive."""

def some_function():
    """Do something which needs to be described in more than one line
    sentence.
    """

def some_function(a):
    """Do something which needs to be described in more than one line
    sentence.

    Args:
        a: Some argument.
    """
```

DON'T:

```python
def my_method_with_BAD_docstring():
    """Method description is short and descriptive.
    """

def my_method_with_another_BAD_docstring():
    """
    Method description is short and descriptive.
    """

def more_complex_method_with_BAD_docstring():
    """Do something which needs to be described in more than one line
    sentence."""

def more_complex_method_with_another_BAD_docstring():
    """Do something which needs to be described in more than one line
       sentence.
    """
```

#### Exceptions

Exception message starts with capital letter and ends with the
exclamation mark.

DO:

```python
raise MyException("Something bad happened!")
```

DON'T:

```python
raise MyException("something bad happened")
```

#### Long string literals

To respect line length limit split long string literals to a series of
literals. Use parentheses to group them when necessary (e.g. in function
call arguments). Keep spaces at the beginning of each string literal
cause it is too easy to loose this space at the end.

DO:

```python
links = graphene.List(
    graphene.NonNull(Link),
    description=(
        "Links between blocks inside the composite. If no arguments"
        " specified then the query simply returns all the links in the"
        " composite block. Parameters allow to select subset of those"
        " links. E.g. it is possible to query for particular links by"
        " specifying their identifiers. It is also possible to get all"
        " the links connected to some particular blocks. If several"
        " arguments specified at the same time then query responds"
        " with a set of links that satisfy all of the specified"
        " criteria."
    ),
    required=True,
)
```

DON'T:

```python
links = graphene.List(
    graphene.NonNull(Link),
    description="Links between blocks inside the composite. If no "
    "arguments specified then the query simply returns all the links "
    "in the composite block. Parameters allow to select subset of "
    "those links. E.g. it is possible to query for particular links by "
    "specifying their identifiers. It is also possible to get all the "
    "links connected to some particular blocks. If several arguments "
    "specified at the same time then query responds with a set of "
    "links that satisfy all of the specified criteria.",
    required=True,
)
```

#### Path-like objects

Use the following approach when you write a function which accepts
path-like objects. This works correctly no matter what kind of path-like
object put as an argument to the function.

```python
import os
from typing import Union

def i_need_path(path: Union[str, os.PathLike]):
    path = os.fspath(path)
    # The `path` is a string with the path.
```