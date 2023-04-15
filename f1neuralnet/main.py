import gym
import f1neuralnet
import pygame
from stable_baselines3 import PPO, A2C


def main():
    env = gym.make('f1neuralnet/F1NeuralNet-v13')
    model = PPO("MlpPolicy", env, verbose=1)
    # model = A2C("MlpPolicy", env, verbose=1, learning_rate=0.001)
    model.learn(100000)
    # env = gym.make('gym_examples/GridWorld-v1')

    # observation, _ = env.reset()
    # env.render()
    # reward = 0

    # while reward < 95:
    #     terminated = False
    #     truncated = False

    #     while not terminated and not truncated:
    #         observation, reward, terminated, truncated, _ = env.step(env.action_space.sample())
    #         env.render()
    #         print(observation)

    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 env.close()

    #     observation, _ = env.reset()

    # env.close()


if __name__ == "__main__":
    main()
