# A Beginner's Guide to Property-Based Testing 

[![CI](https://github.com/meeshkan/introduction-to-property-based-testing/workflows/CI/badge.svg)](https://github.com/meeshkan/introduction-to-property-based-testing/actions?query=branch%3Amaster)
[![Chat on Gitter](https://badges.gitter.im/gitterHQ/gitter.png)](https://gitter.im/meeshkan/community)

This repository contains the source code for our article: [From 1 to 10,000 test cases in under an hour - A beginner's guide to property-based testing]().

Most of the tests are written with [Hypothesis](https://hypothesis.readthedocs.io/en/latest/), a Python library for generative test cases.

If you run into problems or have any questions, please [open an issue](https://github.com/meeshkan/beginners-guide-to-property-based-testing/issues) or [reach out to us on Gitter](https://gitter.im/meeshkan/community).

## Table of Contents
- [Running the tests](#running-the-tests)
- [Available libraries](#available-libraries)
- [More resources](#more-resources)
- [Contributing](#contributing)
- [Tell us what you think](#tell-us-what-you-think)

## Running the tests

⚠️ **Prerequisites**:
- [Python 3+](https://www.python.org/downloads/)

Clone this repository and move into the directory:
```bash
git clone https://github.com/meeshkan/beginners-guide-to-property-based-testing.git
cd beginners-guide-to-property-based-testing
```

Then, run `make`:

```bash
make
```

> This command executes scripts from the [Makefile](./Makefile). These scripts set up a [`venv` directory](https://docs.python.org/3/library/venv.html), install the dependencies and run the tests. It will also automatically format the code using [black](https://black.readthedocs.io/en/stable/) and [isort](https://timothycrosley.github.io/isort/).

After you've run `make` once, you can also execute the tests using the following steps.

Launch your virtual environment:

```bash
. venv/bin/activate
```

> Whenever you're done, you can terminate the virtual environment by running: `deactivate`  

Then, run [pytest](https://pypi.org/project/pytest/):

```bash
pytest
```

You can also run individual tests with:

```bash
pytest file_name.py
```

## Available libraries

- [Hypothesis](https://hypothesis.readthedocs.io/en/latest/): Python (used in our guide)
- [fast-check](https://github.com/dubzzz/fast-check): TypeScript
- [FsCheck](https://fscheck.github.io/FsCheck/): .NET
- [jqwik](https://jqwik.net/): Java
- [PropCheck](https://github.com/alfert/propcheck): Elixir
- [PropEr](https://proper-testing.github.io/): Erlang
- [RapidCheck](https://github.com/emil-e/rapidcheck): C++
- [QuickCheck](https://hackage.haskell.org/package/QuickCheck): Haskell
- [QuickCheck ported to Rust](https://docs.rs/quickcheck/0.9.2/quickcheck/): Rust

## More resources

- 🖥 [Slides and demo from an introduction to property-based testing presentation](https://github.com/ksaaskil/introduction-to-property-based-testing) by our colleague Kimmo Sääskilahti
- 📖 [Introduction to Property Based Testing](https://medium.com/criteo-labs/introduction-to-property-based-testing-f5236229d237) by Nicolas Dubien
- 🔗 [A collection of introductory materials](https://jqwik.net/property-based-testing.html) by jqwik
- 📖 [Property-based Testing Patterns](https://blog.ssanj.net/posts/2016-06-26-property-based-testing-patterns.html) by Sanjiv Sahayam
- 🎥 [Testing the Hard Stuff and Staying Sane](https://www.youtube.com/watch?v=zi0rHwfiX1Q) by John Hughes
- 📖 [Property-based testing: what is it?](https://blog.jessitron.com/2013/04/25/property-based-testing-what-is-it/) by Jessica Joy Kerr

## Contributing

Notice a bug? Interested in adding a new section to our guide? Have any other property-based testing resources you think we should know? The best way to get involved is to [open an issue](https://github.com/meeshkan/beginners-guide-to-property-based-testing/issues).

Please note that this project is governed by the [Meeshkan Community Code of Conduct](https://github.com/meeshkan/code-of-conduct). By participating, you agree to abide by its terms.

## Tell us what you think

At [Meeshkan](https://meeshkan.com/), we're working to improve how people test their products. So no matter if you loved or loathed our guide, we want to hear from you. 

Here are some ways you can get in touch:
- [Open an issue](https://github.com/meeshkan/beginners-guide-to-property-based-testing/issues)
- [Tweet at us](https://twitter.com/meeshkanml)
- [Reach out on Gitter](https://gitter.im/Meeshkan/community)

Some lingering questions we have:
- Why weren't you using property-based testing before?
- After reading through this guide, would you be willing to try? 
- Are you interested in seeing another article expanding on the topic?