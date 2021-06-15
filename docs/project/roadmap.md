# Project's Roadmap

**Warning: This document is only a draft and as such far from being complete. All information described here are subject to change anytime.**

The project will be cut in the four phases described below.

- [Project's Roadmap](#projects-roadmap)
  - [Conception](#conception)
  - [Validation](#validation)
  - [Implementation](#implementation)
  - [Evolution, Optimization & Maintenance](#evolution-optimization--maintenance)

## Conception

Firstly we should write conception documents about the system working or any new feature that we want to introduce and then we should implement those concepts.
I'm writing this document when I've made a stable version of `linekdin-bot` but from now on I will be writing conception documents before coding them.

## Validation

Once all conception documents are ready, they will be validated one by one, and may frozen. Breaking changes after validation are still acceptable but they may lead to re-structuring the software design, that's why we want to write **Software** entities (classes, modules, functions, etc.) that should be open for extension but closed for modification.

## Implementation

Once all documents have been validated, the different project's pieces can be implemented.
It may happen that, during implementation, some validated documents get modifications in order to improve or fix some specific points. Each modification will need to be validated in order to preserve the stability of these documents so we have to give extra focus while writing conception documents.

## Evolution, Optimization & Maintenance

The _Evolution, Optimization & Maintenance_ (EPM) part is pretty explicit: it's all about improving linkedin-bot's existing features, introducing new ones as needed, improving performance and stability, and fixing new bugs.
This part will last forever, as for all other bots.
