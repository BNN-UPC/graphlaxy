#python GraphlaxyDataGen.py optimization optimize -n grid2 -g 2
#python GraphlaxyDataGen.py optimization optimize -n grid4 -g 4
#python GraphlaxyDataGen.py optimization optimize -n grid8 -g 8
#python GraphlaxyDataGen.py optimization optimize -n grid16 -g 16
#python GraphlaxyDataGen.py optimization optimize -n grid32 -g 32
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid2 -F -n grid2 -s 1000 -m
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid4 -F -n grid4 -s 1000 -m
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid8 -F -n grid8 -s 1000 -m
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid16 -F -n grid16 -s 1000 -m
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid32 -F -n grid32 -s 1000 -m
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid2 -m 
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid4 -m
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid8 -m
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid16 -m
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid32 -m
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid2
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid4
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid8
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid16
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid32

#python GraphlaxyDataGen.py optimization optimize -n grid2_v3 -g 2 &
#python GraphlaxyDataGen.py optimization optimize -n grid4_v3 -g 4 &
#python GraphlaxyDataGen.py optimization optimize -n grid16_v3 -g 16 &
#python GraphlaxyDataGen.py optimization optimize -n grid32_v3 -g 32 &
#wait
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid2_v3 -F -n grid2_v3 -s 1000 -m
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid2_v3 -m
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid2_v3
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid4_v3 -F -n grid4_v3 -s 1000 -m
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid4_v3 -m
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid4_v3
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid16_v3 -F -n grid16_v3 -s 1000 -m
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid16_v3 -m
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid16_v3
#python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/grid32_v3 -F -n grid32_v3 -s 1000 -m
#python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/grid32_v3 -m
#python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/grid32_v3

python GraphlaxyDataGen.py optimization optimize -n prec11 -g 8 -p 1e-1 &
python GraphlaxyDataGen.py optimization optimize -n prec52 -g 8 -p 5e-2 &
python GraphlaxyDataGen.py optimization optimize -n prec12 -g 8 -p 1e-2 &
python GraphlaxyDataGen.py optimization optimize -n prec53 -g 8 -p 5e-3 &
wait
python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/prec11 -F -n prec11 -s 1000 -m
python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/prec11 -m
python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/prec11
python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/prec52 -F -n prec52 -s 1000 -m
python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/prec52 -m
python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/prec52
python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/prec12 -F -n prec12 -s 1000 -m
python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/prec12 -m
python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/prec12
python GraphlaxyDataGen.py generate -f ../parameter_tunning_result_datasets/prec53 -F -n prec53 -s 1000 -m
python GraphlaxyDataGen.py optimization metrics -f ../parameter_tunning_result_datasets/prec53 -m
python GraphlaxyDataGen.py statistics -f ../parameter_tunning_result_datasets/prec53

