---
type: news
title: Congratulations Dr. Alper Ahmetoğlu
description: Alper Ahmetoğlu has successfully defended his PhD thesis
featured: true
date: 2024-01-31
thumbnail: uploads/ahmet-alperoglu-doktora.png
---
## Neurosymbolic Representations for Lifelong Learning

### Abstract

This thesis presents a novel framework for robot learning that combines the advantages of deep neural architectures in processing high-dimensional vectors with classical AI search techniques to bridge the gap between continuous sensorimotor data of the robot and domains consisting of finite entities. The aim is to convert information about the environment collected through interactions into an appropriate symbolic form on which a search tree can be built to reach a desired state. The framework consists of an encoder-decoder type of network with binarized activations in the bottleneck layer. The state of the environment, represented as a set of object features, is given to the encoder as input. The output is a discrete vector, treated as the object’s symbol, given to the decoder together with the action vector. The decoder predicts the effect observed by the agent due to the executed action. Once the network is trained, we can transform the continuously represented environment definition into symbolic vectors using the encoder. This allows us to build rules defining the transitions in the environment defined over these symbols. These rules can be translated into planning domain definition language (PDDL), allowing domain-independent off-the-shelf planners to be used to search for a goal state. Our experiments on tabletop object manipulation setups show that the system can learn appropriate symbols of the environment that allow it to build object towers with desired heights and complex object structures that require modeling the relations between objects by reasoning through the rules defined over the symbols learned in an unsupervised manner. As the framework is built with differentiable blocks, it affords appending recent advances in deep learning with ease, allowing it to be extensible in multiple directions.
