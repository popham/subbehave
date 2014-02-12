# Subbehave

The Subbehave module exposes [Behave](http://pythonhosted.org/behave/) step outcomes as commands for consumption by another process.
Additional commands are provided for transitions from feature to scenario and from scenario to step.
A consumer can provide additional commands for Behave to emit.
Behave hooks typically emit these commands to alter the state of the consumer.
A Django-testing consumer, [djbehave](https://github.com/popham/djbehave), was developed in parallel with this module, and this module should serve as a model for additional consumers.
