import os

simulator_settings = {
    "path_to_settings": os.path.join(os.getcwd(), "simulator", "settings"),
    "path_to_models": os.path.join(os.getcwd(), "simulator", "settings", "models"),
    "duration": 20,
    "dt": 0.001,
    "show_plot": True,
    "plot_update_frequency": 1.0
}