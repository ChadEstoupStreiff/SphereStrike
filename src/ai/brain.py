import logging
import os
import random
from typing import List

import numpy as np
import tensorflow as tf
from tensorflow import keras

from core import get_env_values
from game.entities.player import PlayerBrain


class LiteModel:
    @classmethod
    def from_file(cls, model_path):
        return LiteModel(tf.lite.Interpreter(model_path=model_path))

    @classmethod
    def from_keras_model(cls, kmodel):
        converter = tf.lite.TFLiteConverter.from_keras_model(kmodel)
        tflite_model = converter.convert()
        return LiteModel(tf.lite.Interpreter(model_content=tflite_model))

    def __init__(self, interpreter):
        self.interpreter = interpreter
        self.interpreter.allocate_tensors()
        input_det = self.interpreter.get_input_details()[0]
        output_det = self.interpreter.get_output_details()[0]
        self.input_index = input_det["index"]
        self.output_index = output_det["index"]
        self.input_shape = input_det["shape"]
        self.output_shape = output_det["shape"]
        self.input_dtype = input_det["dtype"]
        self.output_dtype = output_det["dtype"]

    def predict(self, inp):
        inp = inp.astype(self.input_dtype)
        count = inp.shape[0]
        out = np.zeros((count, self.output_shape[1]), dtype=self.output_dtype)
        for i in range(count):
            self.interpreter.set_tensor(self.input_index, inp[i : i + 1])
            self.interpreter.invoke()
            out[i] = self.interpreter.get_tensor(self.output_index)[0]
        return out

    def predict_single(self, inp):
        """Like predict(), but only for a single record. The input data can be a Python list."""
        inp = np.array([inp], dtype=self.input_dtype)
        self.interpreter.set_tensor(self.input_index, inp)
        self.interpreter.invoke()
        out = self.interpreter.get_tensor(self.output_index)
        return out[0]


class AIBrain(PlayerBrain):
    def __init__(self) -> None:
        super().__init__()
        self.model = None
        self.load_model()
        logging.debug(self.model)

    def save_model(self):
        if self.model is not None:
            model_folder = os.path.join(
                get_env_values("MODEL_PATH"), get_env_values("MODEL_NAME"), ".cpkt"
            )
            if not os.path.exists(model_folder):
                os.makedirs(model_folder)
            self.model.save(os.path.join(model_folder, "stronger"))

    def load_model(self):
        model_folder = os.path.join(
            get_env_values("MODEL_PATH"), get_env_values("MODEL_NAME"), ".cpkt"
        )
        if os.path.exists(model_folder):
            self.model = LiteModel.from_file(os.path.join(model_folder, "stronger"))
        else:
            self.model = tf.keras.Sequential(
                [
                    keras.layers.Input(shape=(12,)),
                    keras.layers.Normalization(axis=None),
                    keras.layers.Dense(100, "relu"),
                    keras.layers.Dense(20, "softmax"),
                    keras.layers.Dense(60),
                    keras.layers.Dense(3),
                ]
            )
            self.model = LiteModel.from_keras_model(self.model)

    def get_inputs(self, game) -> List[bool]:
        inputs = [False, False, False]

        model_result = self.model.predict_single(
            np.array(
                [
                    game.players[0].X,
                    game.players[0].Y,
                    game.players[0].v_X,
                    game.players[0].v_Y,
                    game.players[1].X,
                    game.players[1].Y,
                    game.players[1].v_X,
                    game.players[1].v_Y,
                    game.balls[0].X,
                    game.balls[0].Y,
                    game.balls[0].v_X,
                    game.balls[0].v_Y,
                ]
            )
        )

        if model_result[0] > 0:
            inputs[0] = True
        if model_result[1] > 0:
            inputs[1] = True
        if model_result[2] > 0:
            inputs[2] = True
        return inputs


class RandomBrain(PlayerBrain):
    def get_inputs(self, _) -> List[bool]:
        inputs = [False, False, False]
        if random.randint(1, 100) <= 5:
            inputs[0] = True
        if random.randint(1, 100) <= 25:
            inputs[1] = True
        if random.randint(1, 100) <= 25:
            inputs[2] = True
        return inputs
