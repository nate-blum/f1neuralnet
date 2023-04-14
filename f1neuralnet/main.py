import gym
import f1neuralnet


def main():
    env = gym.make('f1neuralnet/F1NeuralNet-v11')
    # env = gym.make('gym_examples/GridWorld-v1')

    observation, _ = env.reset()
    env.render()
    reward = 0

    while reward < 95:
        terminated = False
        truncated = False

        while not terminated and not truncated:
            observation, reward, terminated, truncated, _ = env.step(env.action_space.sample())
            env.render()
            print(observation)

        observation, _ = env.reset()

    env.close()


if __name__ == "__main__":
    main()
