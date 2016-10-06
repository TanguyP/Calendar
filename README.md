This document outlines the design planned for the Calendar42 API Proxy.

# Technologies used
* We will use **Django**, which offers a good tradeoff between offering simple setup of a project and providing good maintainability/allowing for future evolutions.
* To ease the development of the API proxy, we will also use the **Django Rest Framework**, for the out-of-the-box security features it provides (authentication, rate limiting) and also because it offers easier evolution of the API (e.g. in case we later want to directly expose Django models through the API).

# Development methodology
An API is a really good candidate for Test-Driven Development, so let's try to write all tests for a given feature before writing any code.

Doing this is also a good way to raise any ambiguities about requirements before starting development. Though I'm confident that in this case the requirements are crystal clear :)

# Architecture
Considering the requirements, we only need a single Django view and URL pattern.
We will use one Django model to store information about an event (ID, title, participants (they don't need their own model, storing them as a string is sufficient for our purposes), cache date).

In theory, Django Rest Framework makes it easy to expose models through a REST API; but as we need custom handling (i.e. call the Calendar42 APIs if we don't have anything cached/if the cache is outdated) we won't use that possibility; instead, we'll implement our own logic for exposing the Event model.

# Security considerations
In order to limit malicious use of the API proxy's resources, we will enforce rate limiting. The rates will be different for authenticated and unauthenticated users.

Since we need authentication, we need access to the same user tokens as the Calendar42 API. For this exercise, we will use the most simple solution: a local file containing the tokens is read by our Django app. The file will obviously not be tracked with Git, so I'll send it by e-mail.

The HTTP request will only be forwarded to the Calendar42 API if the user is authenticated.

Note: in a real-life scenario, the API proxy's limiting rates for authenticated users should always be kept in line with the Calendar42 API's rates. Otherwise, our proxy may allow a user's HTTP request that will in the end be refused by the Calendar42 API, or on the contrary, may block a request that should have been allowed.