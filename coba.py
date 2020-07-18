import csv 

#fuzzyfication
def er(x) :
	e_l =0
	e_s = 0
	e_sh = 0
	e_h = 0
	temp = 0
	#4 klasifikasi low, standard, standard-high, high 
	if (x >= 0 and x <= 2) :
		e_l = 1
	elif (x > 2 and x <= 3) :
		temp = (3-x) 
		e_l = temp/(1)
	elif (x > 3 and x <= 3.5) :
		temp = (x-3) 
		e_s = temp/(0.5)
	elif (x > 3.5 and x <= 5) :
		e_s = 1
	elif (x > 5 and x <=6) : 
		temp = (6-x)
		e_s = temp/(1)
		temp = (x-5)
		e_sh = temp/(1)
	elif (x > 6 and x <= 8) : 
		e_sh = 1
	elif (x >8 and x <=9) :
		temp = (9-x)
		e_sh = temp/(1)
		temp = (x-8) 
		e_h = temp/(1)
	elif (x > 9) :
		e_h = 1
	return e_l, e_s, e_sh, e_h

def fol(y) :
	f_r = 0
	f_c = 0
	f_t = 0
	temp = 0	
	#3 klasifikasi rendah, cukup, tinggi
	if y >= 0 and y <= 25000 :
		f_r = 1
	elif y > 25000 and y <=50000 :
		temp =(50000-y) 
		f_r = temp/(25000)
		temp =(y-25000)
		f_c = (y-25000)/(25000)
	elif y > 50000 and y <= 67000 :
		f_c = 1
	elif y > 67000 and y <= 75000 :
		temp =(75000-y)
		f_c = temp/(80.5)
	elif y > 75000 and y <=  87000 :
		temp = (y-75000)
		f_t = temp/(82000)
	elif y > 87000 :
		f_t = 1
	return f_r, f_c, f_t

#fungsi inferensi, nn untuk mewakili nano, mc untuk mewakili micro, md untuk mewakili medium 
def inference (f_r, f_c, f_t, e_l, e_s, e_sh, e_h):
	nn1,nn2,nn3,mc1,mc2,mc3,mc4,mc5,md1,md2,md3,md4=0,0,0,0,0,0,0,0,0,0,0,0
	if f_r != 0 and e_l != 0 and e_s == 0 and e_sh == 0 and e_h == 0 and f_c == 0 and f_t == 0 :
		nn1 = min(f_r,e_l)
	elif f_r != 0 and e_s != 0 and e_l == 0 and e_sh == 0 and e_h == 0 and f_c == 0 and f_t == 0 :
		nn2 = min (f_r,e_s)
	elif f_r != 0 and e_sh != 0 and e_s == 0 and e_l == 0 and e_h == 0 and f_c == 0 and f_t == 0 :
		mc1 = min(f_r,e_sh)
	elif f_r != 0 and e_h != 0 and e_s == 0 and e_sh == 0 and e_l == 0 and f_c == 0 and f_t == 0:
		mc2 = min(f_r,e_h)
	elif f_c != 0 and e_l != 0 and e_s == 0 and e_sh == 0 and e_h == 0 and f_r == 0 and f_t == 0:
		nn3 = min(f_c,e_l)
	elif f_c != 0 and e_s != 0 and e_l == 0 and e_sh == 0 and e_h == 0 and f_r == 0 and f_t == 0:
		mc3 = min(f_c,e_s)
	elif f_c != 0 and e_sh != 0 and e_s == 0 and e_l == 0 and e_h == 0 and f_r == 0 and f_t == 0:
		md1 = min(f_c,e_sh)
	elif f_c != 0 and e_h != 0 and e_s == 0 and e_sh == 0 and e_l == 0 and f_r == 0 and f_t == 0:
		md2 = min(f_c,e_h)
	elif f_t != 0 and e_l != 0 and e_s == 0 and e_sh == 0 and e_h == 0 and f_c == 0 and f_r == 0:
		mc4 = min(f_t,e_l)
	elif f_t != 0 and e_s != 0 and e_l == 0 and e_sh == 0 and e_h == 0 and f_c == 0 and f_r == 0:
		mc5 = min(f_t,e_s)
	elif f_t != 0 and e_sh != 0 and e_s == 0 and e_sh == 0 and e_h == 0 and f_c == 0 and f_r == 0:
		md3 = min(f_t,e_sh)
	elif f_t != 0 and e_h != 0 and e_s == 0 and e_sh == 0 and e_l == 0 and f_c == 0 and f_t == 0:
		md4 = min(f_t,e_h)
		
	nano = max(nn1,nn2,nn3)
	micro = max(mc1,mc2,mc3,mc4,mc5)
	medium = max (md1,md2,md3,md4)
	return nano,micro,medium

#fungsi defuzzyfication dengan sugeno diset fk singleton 10(nano), 40(micro), 80(medium)
def ystar (nano, micro, medium) :
	final = 0
	if nano!= 0 and micro != 0 :
		temp = (nano*10)+(micro*40)
		final = (temp/(nano+micro))
	elif nano!= 0 and medium != 0 :
		temp = (nano*10)+(medium*80)
		final = (temp/(nano+medium))
	elif micro!= 0 and medium != 0 :
		temp = (micro*40)+(medium*80)
		final = temp/(micro+medium)
	elif micro == 0 and  medium == 0  and nano !=0 :
		temp = (nano*10)
		final = temp/nano
	elif nano == 0 and  medium == 0 and micro !=0:
		temp = (micro*40)
		final = temp/micro
	elif nano == 0 and  micro == 0 and medium != 0 :	
		temp = (medium*80)
		final = temp /medium 
	return final	

inf = []
ER = []
FOL = []
with open('influencers.csv') as File :
	angka = 1
	reader = csv.reader(File, delimiter=',', quotechar = ',', quoting =csv.QUOTE_MINIMAL)
	next(reader)
	for row in reader :
		id, followerCount, engagementRate = row
		angka = 0
		inf.append(row)

lah = []
a = 0
for row in (inf) :
	f1,f2,f3= fol(float(followerCount))
	e1,e2,e3,e4 = er(float(engagementRate))
	hn,hmc,hmd = inference(f1,f2,f3,e1,e2,e3,e4)
	y = ystar(hn,hmc,hmd)
	fin=[]
	fin.append(a+1)
	fin.append(y)
	a = a+1
	lah.append(fin)
print(lah)
print('\n')
print('HASIL YANG SUDAH DI SORTING LALU DIAMBIL 20 TERATAS')
lah.sort(key=lambda x:x[1],reverse=True)
with open ('chosen.csv', 'w') as writeFile :
	w = csv.writer(writeFile)
	w.writerow (['inilah hahaha'])
	for i in range (20) :
		w.writerow (lah[i])
		print(lah[i])

print('SUDAH MASUK KE DALAM CSV')

