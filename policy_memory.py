class ConflictPolicy:
    def __init__(self):
        # initial beliefs (not fixed rules)
        self.weights = {
            "energy": 1.0,
            "integrity": 1.0,
            "progress": 1.0
        }

    def score(self, state, action_effects):
        """
        Higher score = better action
        """
        return (
            self.weights["energy"] * action_effects["energy_delta"] +
            self.weights["integrity"] * action_effects["integrity_delta"] +
            self.weights["progress"] * action_effects["progress_delta"]
        )

    def update(self, experience):
        """
        experience = (state, action, reward)
        Learns which weights produced good outcomes
        """

        reward = experience["reward"]
        effects = experience["effects"]

        # simple gradient-like adjustment
        for k in self.weights:
            self.weights[k] += 0.01 * reward * effects.get(k + "_delta", 0)
