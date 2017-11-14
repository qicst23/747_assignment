
exp_name='gMhrS5u6-Rg'

mkdir -p ../exp/$exp_name ../exp/$exp_name/models/ ../exp/$exp_name/results/ ../exp/$exp_name/reports/ ../exp/$exp_name/logs

for hidden in 32 64 128 256 512 1024
 do
   python 01_predict_codes_exp.py $hidden ../exp/$exp_name
 done
