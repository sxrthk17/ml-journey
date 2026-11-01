# Day 1 — Architectural Audit of `requests`

**Project:** Python Source Code Archaeology  
**Week:** 1  
**Day:** 1  
**Library:** requests  
**Files Audited:** 2  
**Functions Audited:** 7

**Date:** 13 June 2026

## Overview

Today was focused on reading code written by other developers.

The objective was to understand how professional developers write code, how they structure their projects, and why clean, maintainable code is important for anyone who may read or contribute to the codebase in the future.

I cloned the `requests` library from GitHub, a human-friendly HTTP library for Python. My goal was to understand the responsibility of different files and to predict the behavior of the code before reading its implementation. I also wanted to identify what a function does, what assumptions it makes, and what inputs or parameters could potentially break its logic.

Instead of simply studying Python syntax, I focused on understanding how a real-world Python library is designed and organized.

---

## Files Targeted

* `requests/api.py`
* `requests/models.py`

---

## Initial Exploration

I began by scanning both files to get a high-level understanding of their responsibilities within the library.

After building a general overview, I started diving deeper into individual functions and their implementations.

---

## Audit Methodology

For each function studied, I followed the process below:

1. Read the function name and parameters.
2. Predict what the function should do.
3. Read the implementation.
4. Compare my prediction with the actual behavior.
5. Document the gap between my understanding and the real implementation.

This approach forced active reasoning instead of passive reading and helped me think more like an engineer reviewing production code rather than a student reading a tutorial.

---
  ## Investigation 1: The `requests/api.py`: the module that implements Requests API.
 Areas Explored: 
 1. request method : `request(method, url, **kwargs)` which return Session class's session.request method with the parameters.
 2. All the following methods return request just by changing the method parameter that request method accepts for ex: get, post, options,head, put, patch and delete, all these methods take url and **kwargs but return the request method by putting the replacing the method with their method name.

 ## Investigation 2: Read 7 functions from 'requests/models.py` this module contains the object that power Requests.
 Areas Explored:
 1. Request Creation.
 2. URL Processing
 3. Parameter and File Encoding
 4. Registering and Deregistering Hooks
 5. The __init__ method and __repr__ method real work and use.

  ### Prediction Before Explaniation:
  
 #### 1. `path_url(self)`
    - My Prediction: uses URL splitter method to split and store path and query inside the list.
    - Correction: This methods property is to extract the path and query string from the full URL to form specific identifier used in the   HTTP request line. *https://api.com/m1/user?id=3* the method shrinks it down to */m1/user?id=3*
    - Gap Analysis: I understood how we split URL to get exactly what we want for easy access. Also figured out how weak I am at understanding codes written by developers.
 #### 2. `_encode_params()`
      - My Prediction: there are 4 methods in the models.py we use @Overload to Overload the method. I thought that this method encodes dicts/tuples to UTF-8 for posting.
      - Correction: This handles Data Transformation converting python dict, lists of tuples into URL encoded quesry string {'q':'python'} becomes q=python. It checks various input types because web servers expect strict string formats, not complex Python objects.
      - Gap Analysis: Not knowing how @overload decorator works, only saw one method where data from dict/list of tuples format was being encoded and skipped the previous three method signatures.
 #### 3. `_encode_files`
    - My Prediction: Encodes files sent in dict or tuple format
    - Correction: It prepares the binary files for multipart/form-data uploads. Acting as the heart of Hardware Software duality, as it maps the "key"(form field) to the "value"(actual file bytes, filename and headers)
    - Gap Analysis: Understood why multiple condition for checking files are there in order to reduce the error. Got to know the dict version of binary files and why it is important.
  
####  4. `register_hook()` and `deregister_hook`
      - My Prediction: this is like a real- life hook used to hook something on the network or to hook onto a request.
      - Correction: A "hook" in this system is a callback function that allows you to inject logic into reques-response lifecycle.
      - Gap Analysis: How bad I was at predicting the real life hook and HTTP hook similarity. Both of them are different.
  
####  5. `__init__` method from `Request` class
     - My Prediction: from the methods signature it looked like it uses List and Dict comprehensions for data, files, headers, hooks etc.
     - Correction: A __init__ method defines the properties all Requests object must have and sets the initial state by assigning these attributes. Uses the comprehensions to provide a concise and readable way to bundle metadata like headers and paramters into a single object.
     - Gap Analysis: Understood why __init__ is a crucial method. It is a strct chechekd that check wheter all the necessary attributes are filled while intialising an object. Also figured out that __init__ and __new__ are different.
    
####  6. `__repr__` method from `Request` class
     - My Preciction: we use this dunder method to show in which format will user see the object is printed.
     - Correction: This dunder method provides an unambiguous string represenation for inspection and debugging. A Pythonic __repr__ should ideally look like the source code needed to re-create that object.
     - Gap Analysis: __repr__ was not just a represetation of object, it is the key which helps the dubuggers and in production level code it acts like a safe key to adress what needs to be changes while debuggging
  
####  7. `prepare()`
     - Correctly Predicted: this method created a PreparedRequest class. Acts as a state controller that performs the validationa and normalisation of the telemetry before it hits the network socket. By this the library avoids Silent Failures by ensuring data is 100% compilant with HTTP Protocol.
     - Gap Analysis: Confidence boosted when i predicted something and I was real close. This is actual return.
 ---
  ## Investigation 3: The Haunted Bus trap:
  while auditing the code , I searched for protection againsts one of Python's most common bugs:
   ``` python
  def function(arg=None):
     if arg is None: 
     arg = []
  ```
  instead of: 
  ``` python 
    def function(args=[]):
      pass
  ```
   Why This Matters: Using a mutable object as a default parameter causes the same object to be reused across all function calls. 
   The maintainers of `requests` use `None` keywords to prevent the hidden state leakeage.

   Leson Learned: Production code contain invisible safety mechanisms that prevent begs before they occur.

  ## Investigation 4: Python Object Creation Lifecycle.
  I used to think that __init__ is maily used for creating the objects in python but I was unaware.
  the __new__ method creates the object and it runs first and then the __init__ method configures the object after creation and runs secodn.

  This clarified Python's object creation pipeline.

  ## Investigation 5: Memory Efficient Audit
  Also checked whether the library used __slots__ method: No usage of  __slots__ was observed as the mainatainers appear to priorotize Flexibility Extensiibility and Ease of Modification over Max Memory optimisation. 
  This is a real life engineering tradeoff.

## `Artifacts Produced`
  ### File Created:
    week1/day1_reset.py
  ### Contents
    - Manual reimplementation of audited functions
    - prediction logs
    - Source code observation
    - Mutuable default argumentsa analysis
    - Perosnal Notes

## Key Takeaways
 1. Reading production code is fundamentally different from reading tutorail.
 2. Defensive Patterns are everywhere in mature codebases in programming.
 3. Engineering is often about tradeoffs rather than pefect solutions.
 4. Understanding flow and architecture is more valuable than memorising syntax.
 5. Source code is the ultimate documentation


## Chain Progress
this session establised the first link in the chain: Python -> Read Code -> Understand Systems -> Build System.
Day 1 Focused eniterly on the first requirements:
> Learn to *Read* and *Judge*
  

  ---

## Status

* [x] Cloned and explored the `requests` library from GitHub
* [x] Audited `requests/api.py`
* [x] Audited 7 functions from `requests/models.py`
* [x] Created prediction logs before reading implementations
* [x] Compared predictions against production implementations
* [x] Investigated defensive programming patterns
* [x] Investigated the Mutable Default Argument ("Haunted Bus") trap
* [x] Learned the difference between `__new__()` and `__init__()`
* [x] Investigated the use of `__slots__`
* [x] Produced supporting code artifacts in `week1/day1_reset.py`
* [x] Completed first production source code audit

---

## Next Session

* Continue auditing additional functions inside the `requests` library
* Improve prediction accuracy before reading implementations
* Trace the complete request lifecycle from API call to network dispatch
* Investigate how `Session` objects manage state and requests internally
* Document new engineering patterns discovered in production code
* Continue strengthening code-reading and code-review skills

---

## Final Reflection

Today was not about writing code.

It was about learning how to read code written by experienced developers and understanding the reasoning behind their design decisions.

For the first time, I approached a Python library as a system rather than a collection of functions. Instead of asking:

> "How does this syntax work?"

I started asking:

* Why was this function designed this way?
* What problem is this code solving?
* What assumptions does this implementation make?
* What could potentially break this logic?
* What tradeoffs did the maintainers make?

The biggest lesson from today was realizing that production code contains many invisible decisions, safety mechanisms, and engineering tradeoffs that are rarely visible in tutorials.

Reading code is a skill separate from writing code, and it is a skill that must be trained deliberately.

---

## Chain Progress

This session established the first link in the chain:

```text
Python
   ↓
Read Code
   ↓
Understand Systems
   ↓
Build Systems
```

Day 1 focused entirely on the first requirement:

> Learn to Read and Judge production-grade code.

The long-term objective is not only to learn Python syntax but also to develop the ability to read, analyze, understand, and eventually build production-grade software systems.

    

  
  
## Goal Going Forward

The objective is not only to learn Python syntax but also to develop the ability to read, analyze, and understand production-grade code written by experienced developers.


