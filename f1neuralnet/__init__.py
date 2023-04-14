from gym.envs.registration import register

register(
    id='f1neuralnet/F1NeuralNet-v11',
    entry_point='f1neuralnet.agent:TrackEnv',
    max_episode_steps=2100,
)

# register(
#     id='gym_examples/GridWorld-v1',
#     entry_point='f1neuralnet.agent:GridWorldEnv',
#     max_episode_steps=300,
# )