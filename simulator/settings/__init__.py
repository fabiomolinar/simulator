import os

simulator_settings = {
    "path_to_settings": os.path.join(os.getcwd(), "simulator", "settings"),
    "path_to_models": os.path.join(os.getcwd(), "simulator", "settings", "models"),
    "duration": 25,
    "dt": 0.001,
    "show_plot": True,
    "plot_update_frequency": 1.0,
    "quiet": True,
    "performance_meter": {
        "enabled": True,
        "quiet": True,
        "measurements": [
            {
                "class": "Overshoot",
                "name": "overshoot",
                "settings": {
                    "Y": {
                        "object_name": "rl",
                        "attribute": "Vr"
                    },
                    "SP": {
                        "object_name": "sig",
                        "attribute": "current_value"
                    }
                }
            },
            {
                "class": "SettlingTime",
                "name": "settling_time",
                "settings": {
                    "Y": {
                        "object_name": "rl",
                        "attribute": "Vr"
                    },
                    "SP": {
                        "object_name": "sig",
                        "attribute": "current_value"
                    },
                    "dx_threshold": 0.001,
                    "dx_cycles_hold": 1000,
                    "range": 0.02
                }
            }
        ]
    }
}