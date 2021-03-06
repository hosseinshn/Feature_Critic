import argparse
import os
os.environ['CUDA_VISIBLE_DEVICES'] = '1'

from model_VD import Model_Feature_Critic_VD
from model_PACS import Model_Feature_Critic_PACS
import sys
import torch
sys.setrecursionlimit(1000000)
import warnings
warnings.filterwarnings("ignore")
torch.set_num_threads(8)

def main():
    train_arg_parser = argparse.ArgumentParser()
    train_arg_parser.add_argument("--dataset", type=str, default='PACS',
                                  help='VD')
    train_arg_parser.add_argument("--method", type=str, default='Feature_Critic',
                                  help='Feature_Critic')
    args = train_arg_parser.parse_args()

    if args.dataset == 'VD':
        '''
           # Designs of dg (auxiliary loss) function
           (1) MLP:  1/M(all MLP(F))
           (2) Flatten mode of FTF
           Flatten = torch.matmul(torch.transpose(feat_a, 0, 1), feat_a).view(1,-1) 
           '''
        train_arg_parser.add_argument("--type", type=str, default='MLP',
                                      help='the type of dg functions, {MLP: 1, Flatten_FTF: 2}')
        train_arg_parser.add_argument("--batch_size", type=int, default=64,
                                      help="batch size for training, default is 64")
        train_arg_parser.add_argument("--batch_size_metatest", type=int, default=32,
                                      help="batch size for meta testing, default is 32")
        train_arg_parser.add_argument("--num_classes", type=int, default=10,
                                      help="number of classes")
        train_arg_parser.add_argument("--iteration_size", type=int, default=30000,
                                      help="iteration of training domains")
        train_arg_parser.add_argument("--lr", type=float, default=5e-4,
                                      help='learning rate of the model')
        train_arg_parser.add_argument("--beta", type=float, default=100,
                                      help='learning rate of the dg function')
        train_arg_parser.add_argument("--heldout_p", type=float, default=1000,
                                      help='learning rate of the heldout function')
        train_arg_parser.add_argument("--omega", type=float, default=1e-4,
                                      help='learning rate of the omega function')
        train_arg_parser.add_argument("--meta_iteration_size", type=int, default=1,
                                      help='iteration of test domains')
        train_arg_parser.add_argument("--logs", type=str, default='logs/VD/Feature_Critic/',
                                      help='logs folder to write log')
        train_arg_parser.add_argument("--load_path", type=str, default='model_output/VD/baseline/',
                                      help='folder for loading baseline model')
        train_arg_parser.add_argument("--model_path", type=str, default='model_output/VD/Feature_Critic/',
                                      help='folder for saving model')
        train_arg_parser.add_argument("--debug", type=bool, default=True,
                                      help='whether for debug mode or not')
        train_arg_parser.add_argument("--count_test", type=int, default=1,
                                      help='the amount of episode for testing our method')
        train_arg_parser.add_argument("--if_train", type=bool, default=False,
                                      help='if we need to train to get the model')
        train_arg_parser.add_argument("--if_test", type=bool, default=True,
                                      help='if we want to test on the target data')
        args = train_arg_parser.parse_args()

        # dg_function = {'1': 'MLP', '2': 'Flatten_FTF'}
        dg_function = {'1': 'MLP'}
        for nn in range(len(dg_function)):
            args.type = dg_function[str(nn + 1)]
            for i in range(args.count_test):
                print('Episode %d in type %s.' % (i, args.type))
                model_obj = Model_Feature_Critic_VD(flags=args)
                if args.if_train == True:
                    model_obj.train(flags=args)
                    torch.cuda.empty_cache()
                if args.if_test == True:
                    model_obj.heldout_test(flags=args)


    if args.dataset == 'PACS':

        train_arg_parser.add_argument("--type", type=str, default='MLP',
                                      help='the type of dg functions, {MLP: 1, Flatten_FTF: 2}')
        train_arg_parser.add_argument("--unseen_index", type=int, default=1,
                                      help="index of unseen domain")
        train_arg_parser.add_argument("--batch_size", type=int, default=32,
                                      help="batch size for training, default is 64")
        train_arg_parser.add_argument("--batch_size_metatest", type=int, default=16,
                                      help="batch size for training, default is 32")
        train_arg_parser.add_argument("--num_classes", type=int, default=7,
                                      help="number of classes")
        train_arg_parser.add_argument("--iteration_size", type=int, default=45000,
                                      help="iteration of training domains")
        train_arg_parser.add_argument("--lr", type=float, default=5e-4,
                                      help='learning rate of the model')
        train_arg_parser.add_argument("--beta", type=float, default=0.01,
                                      help='learning rate of the dg function')
        train_arg_parser.add_argument("--heldout_p", type=float, default=1,
                                      help='learning rate of the heldout function')
        train_arg_parser.add_argument("--omega", type=float, default=1e-3,
                                      help='learning rate of the omega function')
        train_arg_parser.add_argument("--meta_iteration_size", type=int, default=1,
                                      help='iteration of test domains')
        train_arg_parser.add_argument("--logs", type=str, default='logs/PACS/Feature_Critic/A/',
                                      help='logs folder to write log')
        train_arg_parser.add_argument("--load_path", type=str, default='model_output/PACS/Baseline/A/',
                                      help='folder for loading baseline model')
        train_arg_parser.add_argument("--model_path", type=str, default='model_output/PACS/Feature_Critic/A/',
                                      help='folder for saving model')
        train_arg_parser.add_argument("--debug", type=bool, default=True,
                                      help='whether for debug mode or not')
        train_arg_parser.add_argument("--count_test", type=int, default=1,
                                      help='the amount of episode for testing our method')
        train_arg_parser.add_argument("--if_train", type=bool, default=False,
                                      help='if we need to train to get the model')
        train_arg_parser.add_argument("--if_test", type=bool, default=True,
                                      help='if we want to test on the target data')
        args = train_arg_parser.parse_args()

        # dg_function = {'1': 'MLP', '2': 'Flatten_FTF'}
        dg_function = {'1': 'MLP'}
        for nn in range(len(dg_function)):
            args.type = dg_function[str(nn + 1)]
            for i in range(args.count_test):
                print('Episode %d in type %s.' % (i, args.type))
                model_obj = Model_Feature_Critic_PACS(flags=args)
                if args.if_train == True:
                    model_obj.train(flags=args)
                    torch.cuda.empty_cache()
                if args.if_test == True:
                    model_obj.heldout_test(flags=args)


if __name__ == "__main__":
    main()
