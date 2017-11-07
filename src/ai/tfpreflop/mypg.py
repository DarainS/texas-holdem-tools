from RL_brain import PolicyGradient
import matplotlib.pyplot as plt
import numpy as np

actions = ['fold', 'call', 'raise']
RL = PolicyGradient(
    n_actions=len(actions)
n_features = len(actions)
learning_rate = 0.02,
                reward_decay = 0.995,
# output_graph=True,
)

for i_episode in range(1000):

    while True:

        action = RL.choose_action(observation)

        observation_, reward, done, info = env.step(action)  # reward = -1 in all cases

        RL.store_transition(observation, action, reward)

        if done:
            # calculate running reward
            ep_rs_sum = sum(RL.ep_rs)
            if 'running_reward' not in globals():
                running_reward = ep_rs_sum
            else:
                running_reward = running_reward * 0.99 + ep_rs_sum * 0.01
            if running_reward > DISPLAY_REWARD_THRESHOLD: RENDER = True  # rendering

            print("episode:", i_episode, "  reward:", int(running_reward))

            vt = RL.learn()  # train

            if i_episode == 30:
                plt.plot(vt)  # plot the episode vt
                plt.xlabel('episode steps')
                plt.ylabel('normalized state-action value')
                plt.show()

            break

        observation = observation_
