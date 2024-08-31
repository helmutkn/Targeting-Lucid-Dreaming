import os

import numpy as np
import torch

from models.main_model import MainModel


class SleePyCoInference:
    def __init__(self, fold, config):
        self.fold = fold

        self.cfg = config
        self.ds_cfg = config['dataset']
        self.fp_cfg = config['feature_pyramid']

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print('[INFO] Config name: {}'.format(config['name']))

        self.train_iter = 0
        self.model = self.build_model()

        self.ckpt_path = os.path.join(os.getcwd(), 'scripts/SleepScoring/SleePyCo/SleePyCo/checkpoints', config['name'])
        self.ckpt_name = 'ckpt_fold-{0:02d}.pth'.format(self.fold)

    def build_model(self):
        model = MainModel(self.cfg)
        print('[INFO] Number of params of model: ', sum(p.numel() for p in model.parameters() if p.requires_grad))
        model = torch.nn.DataParallel(model, device_ids=[0])
        load_path = os.path.join(os.getcwd(), 'scripts/SleepScoring/SleePyCo/SleePyCo', 'checkpoints', self.cfg['name'], 'ckpt_fold-{0:02d}.pth'.format(self.fold))
        model.load_state_dict(torch.load(load_path, map_location=torch.device('cpu')), strict=False)
        print('[INFO] Model loaded')
        model.to(self.device)
        print('[INFO] Model prepared, Device used: {} GPU: cpu'.format(self.device))

        return model

    @torch.no_grad()
    def evaluate(self, input_data):
        inputs = torch.tensor(input_data, dtype=torch.float32).to(self.device)
        self.model.eval()

        outputs = self.model(inputs)
        outputs_sum = torch.zeros_like(outputs[0])

        for output in outputs:
            outputs_sum += output

        predicted = torch.argmax(outputs_sum, 1)

        return predicted

    def infere(self, input_data):
        # input_data has to be tensor of shape (1,1,x) where x is the 30 second epoch * sample_rate
        prediction = self.evaluate(input_data)
        return prediction

    def run(self):
        self.model.load_state_dict(torch.load(os.path.join(self.ckpt_path, self.ckpt_name), map_location=torch.device('cpu')))
        input_data = np.random.rand(1, 1, 30*256)
        prediction = self.evaluate(input_data)
        print('')
        return prediction
