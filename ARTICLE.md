---
title: From 10 to 1,000,000 test cases in under an hour: A beginner's guide to property-based testing 
description: This guide walks you through the what and why of property-based testing, with practical use cases and examples along the way. 
author: Fredrik Fornwall
authorLink: https://dev.to/fornwall
tags:
  - testing
  - tutorial
  - beginners
  - python
---

<!-- TODO: INTRODUCTION SENTENCE 🙆‍♀️ -->

Maybe you've written unit tests before, but this is the first time you've heard about property-based testing. Or maybe you've heard the term, but still don't really get what it's about. Either way, we've got you. 

In this guide, we'll cover the fundamentals of property-based testing and how it differs from traditional example-based testing practices. We'll walk you through practical examples of properties and how to write tests that address them. Finally, we'll learn how to use property-based testing to find bugs in our code and what existing libraries are out there. 

## What's in this guide

- [Traditional unit tests based on examples](#traditional-unit-tests-based-on-examples)
    - [Limitations of example-based testing](#limitations-of-example-based-testing)
- [Introduction to property-based testing](#introduction-to-property-based-testing)
    - [An example using Hypothesis](#an-example-using-hypothesis)
    - [What can be a property?](#what-can-be-a-property)
    - [How does property-based testing differ from example-based?](#how-does-property-based-testing-differ-from-example-based)
- [Example properties and how to test for them](#example-properties-and-how-to-test-for-them)
    - [Unexpected exceptions should never be thrown](#unexpected-exceptions-should-never-be-thrown)
    - [Values shouldn't change after encoding and then decoding](#values-shouldnt-change-after-encoding-and-then-decoding)
    - [A naive method should still give the same result](#a-naive-method-should-still-give-the-same-result)
- [Finding bugs with property-based testing](#finding-bugs-with-property-based-testing)
- [Available libraries](#available-libraries)
- [Conclusion](#conclusion)

⚠️ **Prerequisites**:
- A general understanding of what unit tests are.
- (Optional) [Python 3+](https://www.python.org/downloads/)* if you want to follow along in your own IDE. 

_* This guide will use Python for code examples, but the concepts aren't limited to Python specifically. So even if you don't know Python, we'd encourage you to read along anyway._

💻 **References**:
We've created a [GitHub repository](github.com/meeshkan/introduction-to-property-based-testing) to accompany this guide. All of the featured code samples exist there as unit tests and include instructions for how to execute them.

## Traditional unit tests based on examples

Most often, software testing is done using **example-based testing**. This means you test that for a given argument, you get a known return value. This return value is known because, well, you provided that value as a sample. So when the you run the function or test system, it then asserts the actual result against that sample return value.

Let's look at an example. Say we wanted to write a function called `sort_this_list` that takes a [list](https://docs.python.org/3/tutorial/introduction.html#lists) as an argument and returns the same list organized in ascending order. To do this, we'll use the built-in Python [`sorted`](https://docs.python.org/3/library/functions.html#sorted) function.

It might look like the following:

```python
def sort_this_list(input_list):
    sorted_list = sorted(input_list)
    return sorted_list
```

Now that we have our `sort_this_list` function, let's test it. 

To test this using example-based testing, we need to provide the test function with return values that we know will be `True`. For example, the list `[5, 3, 1, 4, 2]` should return `[1, 2, 3, 4, 5]` after it's sorted.

```python
# Test for our function that uses two manually determined return values:
def test_sort_this_list():
    assert sort_this_list([5, 3, 1, 4, 2]) == [1, 2, 3, 4, 5] # True
    assert sort_this_list(['a', 'd', 'c', 'e', 'b']) == ['a', 'b', 'c', 'd', 'e'] # True
```

And with that, we have a passing example-based test 🎉

### Limitations of example-based testing

While example-based tests work well in many situations and provide an (arguably) low barrier of entry to testing, they do have downsides. Particularly that you have to manually create every return value - and you can only test as many values as you're willing to write. The less we write, the more likely it is that our tests miss catching bugs in our code.

To show why this could be a problem, let's look at the test for the `sort_this_list` function from the last section:

```python
def test_sort_this_list():
    assert sort_this_list([5, 3, 1, 4, 2]) == [1, 2, 3, 4, 5] # True
    assert sort_this_list(['a', 'd', 'c', 'e', 'b']) == ['a', 'b', 'c', 'd', 'e'] # True
```

Both of these assertions return `True`. So if you only tested these two values, you might believe that the `sort_this_list` function always returns the desired result.

However, if we add a third value:

```python
def test_sort_this_list():
    assert sort_this_list([5, 3, 1, 4, 2]) == [1, 2, 3, 4, 5] 
    assert sort_this_list(['a', 'd', 'c', 'e', 'b']) == ['a', 'b', 'c', 'd', 'e'] 
    # Add a new test case:
    assert sort_this_list(['a', 2, 'c', 3, 'b', 1]) == ['a', 'b', 'c', 1, 2, 3]
```

And then run the test... we hit an error:

```bash
TypeError: '<' not supported between instances of 'int' and 'str'
```

Turns out our `sort_this_list` function doesn't work properly when the list contains both integers and strings. Maybe you already knew that, but maybe we would've never known that without a specific test case. 

Even with these limitations, example-based testing will continue to be the norm in software testing. Throughout the rest of this guide, though, we'll explore an additional technique designed to compliment your existing (likely example-based) tests and enhance the test coverage of your code.

## Introduction to property-based testing

When we think about the limitations of example-based testing, many questions come to mind. What if we want to test hundreds (or millions) of test cases? Or possibly ones we could never dream of coming up with ourselves? 

**Property-based testing** is a different approach here to help with that. With property-based testing, you don't generate the exact values manually. Instead, that is done by a computer automatically. 

As the developer, what you have to do is:

- Specify what value to generate.
- Assert on guarantees (or **properties**) that are true regardless of the exact value.

### An example using Hypothesis

To put property-based testing into practice, let's look at an example using [Hypothesis](https://hypothesis.readthedocs.io/en/latest/), a Python library for generative test cases. We chose Hypothesis mostly because we're using Python - but also because the documentation is clear and thorough. 

We'll use our `sort_this_list` function from earlier. As a reminder, here's what that looked like:

```python
def sort_this_list(input_list):
    sorted_list = sorted(input_list)
    return sorted_list
```

Now let's write our property-based tests using Hypothesis. To limit the scope, we'll only test for lists of integers:

```python
# test_sorted_list.py
import hypothesis.strategies as some
from hypothesis import given

# Use the @given indicator to guide Hypothesis to what input value we need:
@given(input_list=some.lists(some.integers()))
def test_sort_this_list_properties(input_list):
    sorted_list = sorted(input_list)
    return sorted_list

    # Regardless of input, sorting should never change the size:
    assert len(sorted_list) == len(input_list)

    # Regardless of input, sorting should never change the set of distinct elements:
    assert set(sorted_list) == set(input_list)

    # Regardless of input, each element in the sorted list should be
    # lower or equal to the value that comes after it:
    for i in range(len(sorted_list) - 1):
        assert sorted_list[i] <= sorted_list[i + 1]
```

> If you're following along on your machine, make sure to install [Hypothesis](https://hypothesis.readthedocs.io/en/latest/quickstart.html#installing) and then you can run the tests using [pytest](https://pypi.org/project/pytest/).

And there you have it, your first property-based test 🎉

What's especially important here is the use of the [@given](https://hypothesis.readthedocs.io/en/latest/details.html#hypothesis.given) function decorator:

```python
@given(input_list=some.lists(some.integers()))
```

This specifies that we want a list of random integers as the input value and **asserts on properties that are true regardless of the exact input**.

If we add a `print(input_list)` statement, we can peek at the _100 different generated input values_:

```
[]
[92]
[66, 24, -25219, 94, -28953, 31131]
[-16316, -367479896]
[-7336253322929551029, -7336253322929551029, 27974, -24308, -64]
...
```

The number of runs and specifics of the generated data can be configured. More on that later on.

### What can be a property?

<!-- TODO: WRITE THIS 😩 -->

### How does property-based testing differ from example-based?

While they originate from different concepts, a property-based test shares many characteristics with how an example-based test is written. This is illustrated in the following comparison of steps:

| Example based                          | Property based                               |
| -------------------------------------- | -------------------------------------------- |
| 1. Set up some example data            | 1. Define data type matching a specification |
| 2. Perform some operations on the data | 2. Perform some operations on the data       |
| 3. Assert something about the result   | 3. Assert properties about the result        |

There are several instances where it would be worthwhile to use property-based testing. But the same can be said for example-based testing. They can, and very likely will, co-exist in the same codebase. So if you were stressed about having to rewrite your entire test suite to try out property-based testing, don't worry. We wouldn't recommend that. 

## Example properties and how to test for them

By now, we've written our first property-based test. And while we're proud of our elegantly sorted lists, this example isn't representative of how you'd use property-based testing out in the real world. So we've gathered three example properties and in this section, we'll guide you through how they might be used to test our software.

All of the examples will continue to use the [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) testing library and its [@given](https://hypothesis.readthedocs.io/en/latest/details.html#hypothesis.given) function decorator.

### Unexpected exceptions should never be thrown

Something that was tested by default in the previous `test_sorted_list_properties` function was that the code didn't throw any exceptions. The fact that the code doesn't throw any exceptions (or more generally, only expected and documented exceptions, and that it never causes a segmentation fault) is a property. And this property can be a convenient one to test, especially if the code has a lot of internal assertions.

As an example, we'll use the [`json.loads`](https://docs.python.org/3/library/json.html#json.loads) function from the Python standard library. Let's test that the `json.loads` function never throws any exceptions other than `json.JSONDecodeError` - regardless of input:

```python
@given(some.text())
def test_json_loads(input_string):
    try:
        json.loads(input_string)
    except json.JSONDecodeError:
        return
```

When we run our test file, it passes 🎉 So what we believed held up under testing!

### Values shouldn't change after encoding and then decoding

A commonly tested property is called symmetry. Symmetry proves in certain operations that decoding an encoded value always results in the original value.

Let's apply it to [base32-crockford](https://github.com/jbittel/base32-crockford), a Python library for the [Base32](https://www.crockford.com/base32.html) encoding format:

```python
@given(some.integers(min_value=0))
def test_base32_crockford(input_int):
      assert base32_crockford.decode(base32_crockford.encode(input_int)) == input_int
```

Because this decoding scheme only works for non-negative integers, we need to specify the _generation strategy_ of our input data. That's why we add `some.integers(min_value=0)` to our `@given` decorator - it restricts Hypothesis to only generate integers with a minium value of zero.

Once again, the test passes 🎉

### A naive method should still give the same result

Sometimes, we can get the desired solution through a naive, unpractical way that isn't acceptable to use in production code. This might be due to the execution time being too slow, memory consumption being too high or it requiring special dependencies that aren't acceptable to install in production.

For example, consider counting the number of set bits in an (arbitrary sized) integer, where we have an optimized solution from the [pygmp2](https://gmpy2.readthedocs.io/en/latest/) library.

Let's compare this with a slower solution that converts the integer to a binary string (using the [bin](https://docs.python.org/3/library/functions.html#bin) function in the Python standard library) and then counts the occurences of the string `"1"` inside of it:

```python
def count_bits_slow(input_int):
    return bin(input_int).count("1")

@given(some.integers(min_value=0))
@settings(max_examples=500)
def test_gmpy2_popcount(input_int):
    assert count_bits_slow(input_int) == gmpy2.popcount(input_int)
```

For illustrative purposes, we've also specified a [`@settings(max_examples=500)`](https://hypothesis.readthedocs.io/en/latest/settings.html) decorator to tweak the default number of input values to generate.

The test passes  🎉 - showing that the optimized, hard-to-follow code of `gmpy2.popcount` gives the same results as our slower but less complex `count_bits_slow` function. 

Be sure to note that if this was the only reason to bring in gmpy2 as a dependency, it'd be wise to benchmark if the performance improvements of it really would outweight the cost and weight of the dependency.

## Finding bugs with property-based testing

We've gone over the concepts of property-based testing and seen various properties in action - this is great. But one of the selling points of property-based tests is that they are supposed help us find more bugs. And we haven't found any bugs yet.

So let's go hunting. 

For this example, we'll use the [json5](https://pypi.org/project/json5/) library for [JSON5](https://json5.org/) serialization. It's a bit niche, sure, but it's also a younger project. This means that we're more likely to uncover a bug compared to a more established library. 

The json5 library contains: 

- One **property** of JSON5 is that it is a superset of JSON.
- Another **property** (which is true of most serialization formats) is that deserializing a serialized string should give us back the original object.

Let's use those properties in a test:

```python
import json
from string import printable

import hypothesis.strategies as some
import json5
from hypothesis import example, given, settings

# Construct a generator of arbitrary objects to test serialization on:
some_object = some.recursive(
    some.none() | some.booleans() | some.floats(allow_nan=False) | some.text(printable),
    lambda children: some.lists(children, min_size=1)
    | some.dictionaries(some.text(printable), children, min_size=1),
)

@given(some_object)
def test_json5_loads(input_object):
    dumped_json_string = json.dumps(input_object)
    dumped_json5_string = json5.dumps(input_object)

    parsed_object_from_json = json5.loads(dumped_json_string)
    parsed_object_from_json5 = json5.loads(dumped_json5_string)

    assert parsed_object_from_json == input_object
    assert parsed_object_from_json5 == input_object
```

After creating a `some_object` generator of [arbitrary objects](https://hypothesis.readthedocs.io/en/latest/data.html#recursive-data), we can verify aspects of the previously mentioned properties: We serialize the input using both `json` and `json5`. Then, we deserialize those two objects back using the `json5` library and assert that the original object was obtained.

But we run into a problem. At the `json5.dumps(input_object)` statement, we get an exception inside the internals of the `json5` library:

```python
    def _is_ident(k):
        k = str(k)
>       if not _is_id_start(k[0]) and k[0] not in (u'$', u'_'):
E       IndexError: string index out of range
```

Besides showing the stack trace as usual, we also get an informative message showing the failed _hypothesis_ - or the generated data that caused our test to fail:

```
# ------------- Hypothesis ------------- #
Falsifying example: test_json5_loads(
    input_object={'': None},
)
```

Using the `{'': None}` input data caused [the issue that we promptly reported](https://github.com/dpranke/pyjson5/issues/37) and [fixed the bug](https://github.com/dpranke/pyjson5/pull/38), which has since been released in version 0.9.4 of the json5 library.

> We want to add that the fix was merged and released within 20 minutes of reporting. Very impressive work by json5 maintainer [@dpranke](https://github.com/dpranke) 👏

But what about the future, how can we be sure that the problem never resurfaces? 

Because the data we are currently generating contained the troublesome input (`{'': None}`), we want to ensure that this input is always used. This should be true even if someone tweaks the `some_object` generator or updates the version of Hypothesis used.

Here, we've used the [@example](https://hypothesis.readthedocs.io/en/latest/reproducing.html#hypothesis.example) decorator to add a hard-coded example in addition to the generated input:

```diff
--- test_json5_decode_orig.py	2020-03-27 09:48:24.000000000 +0100
+++ test_json5_decode.py	2020-03-27 09:48:32.000000000 +0100
@@ -14,6 +14,7 @@
 
 @given(some_object)
 @settings(max_examples=500)
+@example({"": None})
 def test_json5_loads(input_object):
     dumped_json_string = json.dumps(input_object)
     dumped_json5_string = json5.dumps(input_object)
```

Bug found ✅ Bug fixed ✅ We're good to go 🎉

## Available libraries

This guide has been using the [Hypothesis](https://hypothesis.readthedocs.io/en/latest/) library for Python. There's a lot of functionality that we haven't covered and, as previously mentioned, the documentation is well-written. So we'd recommmend checking it out if you're a Python user.

There are also several other libraries built for property-based testing, in a vareity of languages. Here are some alternatives:

- [fast-check](https://github.com/dubzzz/fast-check): TypeScript
- [FsCheck](https://fscheck.github.io/FsCheck/): .NET
- [jqwik](https://jqwik.net/): Java
- [PropCheck](https://github.com/alfert/propcheck): Elixir
- [PropEr](https://proper-testing.github.io/): Erlang
- [RapidCheck](https://github.com/emil-e/rapidcheck): C++
- [QuickCheck](https://hackage.haskell.org/package/QuickCheck): Haskell
- [QuickCheck ported to Rust](https://docs.rs/quickcheck/0.9.2/quickcheck/): Rust

## Conclusion

<!-- TODO: FINISH THIS 😴 -->

At [Meeshkan](https://meeshkan.com/) we are working on improving how people test systems. Follow us at https://twitter.com/meeshkanml or reach out to us on https://gitter.im/Meeshkan/community!

Why are you not using property based testing? Interested in seeing another article expanding on the topic? Let us know in the comments!
