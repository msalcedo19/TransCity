from enum import Enum
import json


class Action(Enum):
    CLOSE_BUS = 'CLOSE_BUS'
    OPEN_BUS = 'OPEN_BUS'
    SEND_BUS = 'SEND_BUS'
    CLOSE_STATION = 'CLOSE_STATION'
    OPEN_STATION = 'OPEN_STATION'


class States(Enum):
    FULL_BUS = 'FULL_BUS'
    FULL_STATION = 'FULL_STATION'
    RELEASE_BUS = 'RELEASE_BUS'
    RELEASE_STATION = 'RELEASE_STATION'


class RL:

    def __init__(self):
        self.brain = {}
        self.train = {}

    def processing(self, file):

        def add_new_action_in_actions(p_actions: dict, new_action: str):
            if p_actions.get(new_action):
                p_actions[new_action] += 1
            else:
                p_actions[new_action] = 1

        def add_new_actions_in_state(p_actions: list, p_new_actions: dict):

            if len(p_actions) > 0:
                for actions_dict in p_actions:
                    if actions_dict.keys() == p_new_actions.keys():
                        for key in p_new_actions.keys():
                            actions_dict[key] += 1
                    else:
                        p_actions.append(p_new_actions)
                        break
            else:
                p_actions.append(p_new_actions)

        with open(file) as infile:
            state_act = None
            new_actions = {}
            for line in infile.readlines():
                line = line.replace("\'", "\"")
                if "\n" in line:
                    line = line.split("\n")[0]
                line_dict: dict = json.loads(line)
                if line_dict.get('state') and line_dict['state'] in self.brain.keys():
                    if state_act:
                        add_new_actions_in_state(self.brain[state_act], new_actions)
                    state_act = line_dict['state']
                    new_actions = {}
                elif line_dict.get('state') and line_dict['state'] not in self.brain.keys():
                    if state_act:
                        add_new_actions_in_state(self.brain[state_act], new_actions)
                    self.brain[line_dict['state']] = []
                    state_act = line_dict['state']
                    new_actions = {}
                elif line_dict.get('action'):
                    add_new_action_in_actions(new_actions, line_dict['action'])
            add_new_actions_in_state(self.brain[state_act], new_actions)

    def training(self):
        for p_state in self.brain.keys():
            p_actions: list = self.brain.get(p_state)
            maxi = 0
            for p_action in p_actions:
                weight = 0
                arr = []
                for pp_action in p_action.keys():
                    # print(p_action[pp_action])
                    weight += p_action[pp_action]
                    arr.append(pp_action)
                if weight > maxi:
                    self.train[p_state] = arr
                    maxi = weight






