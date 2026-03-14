from openwakeword.train import train
import os

train(
    model_name="alpha",
    positive_reference_clips=[r"C:\ALPHA\wakeword_training\positive"],
    output_dir=r"C:\ALPHA\wakeword_training\model",
    n_epochs=100,
)
print("Training complete!")
