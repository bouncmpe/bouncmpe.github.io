---
type: news
title: Yavuz Köroğlu defended his Phd thesis
date: 2022-07-25
thumbnail: https://picsum.photos/seed/4/1280/720
---

Underestimating the value of software testing had catastrophic results in recent
history. Automated Test Generation (ATG) is an approach that aims to minimize
the manual effort required for testing. This thesis aims to improve the
effectiveness and performance of ATG approaches via Machine Learning (ML) based
guidance, and focuses on Android Graphical User Interface (GUI) testing using
Reinforcement Learning (RL), specifically. We propose four solutions, Q-learning
Based Exploration (QBE), Test Case Mutation (TCM), Fully Automated Reinforcement
LEArning Driven (FARLEAD), and FARLEAD2 test generators. QBE uses RL to crawl a
set of applications and learns an action generation policy while exploring.
Then, it uses this learned policy to either detect more unique crashes or cover
more activities in new applications. TCM takes the tests QBE generates and
replaces the well-behaving actions in those tests with bad-behaving ones to
detect even more crashes. FARLEAD uses RL to learn how to verify a functional
behavior that is given as a high-level test scenario in the form of a
monitorable formal specification. FARLEAD learns by trial-and-error like QBE but
it learns app-specific patterns instead of QBE's app-generic patterns. To the
best of out knowledge, FARLEAD is the first engine fully automating the
functional testing of GUI applications. Finally, FARLEAD2 improves FARLEAD with
Generalized Experience Replay (GER) and human-readable Staged Test Scenario
(STS) language.Experimental results show that, QBE outperforms state-of-the-art
test generators in crash detection and coverage. Furthermore, executing QBE
first and then switching to TCM detects even more unique crashes. FARLEAD and
FARLEAD2 expand the scope of automated testing to verifying functional behavior.
Overall, these test generators elevate automated GUI testing closer to replacing
manual GUI testing.
