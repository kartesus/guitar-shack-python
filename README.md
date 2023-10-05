# Guitar Shack Legacy Kata

This is inspired by Jason Gorman's [original Kata in Java](https://github.com/jasongorman/guitar_shack_legacy_java).

The code represents a monolithic "ball of mud" application that sends notifications to the owners of a guitar shop when
stock levels are low. The code has a business purpose, which is to replenish stock in an optimal way, such that we never
run out of stock, but also don't have too much stock.

## The Problem

Last thirty days sales data has not been the best predictor of future sales, so we need to improve the algorithm. Being
a
ball of mud, the code is difficult to change. We need to refactor the code to make it easier to change, and then we can
improve the algorithm.

Improving this algorithm is a continuous process, so we need to be able to make changes to the code easily. We also need
to be able to support multiple algorithms, so that we can compare the results of different algorithms.

## Collaboration-Driven Design (London School TDD)

We focus on collaboration between components and the domain model is an emergent property of that collaboration.
This approach is very in tune with layered architectures, as we design one layer at a time in isolation by mocking its
collaborators.

## State-Driven Design (Chicago School TDD)

The domain model is the primary focus of the design, especially its state transitions. This architecture is more aligned
with concentric architectures, where the domain model is at the centre, and the layers are built around it.