import sys
##Main Program
if len(sys.argv) < 3:
	print "Error\nPlease use the format: python bayes.py -i input_filename\n"
	quit()
if sys.argv[1] == '-i' :
	print "Opening File", str(sys.argv[2])
	f = open(str(sys.argv[2]),'r')
else:
	print "Error\nPlease use the format: python bayes.py -i input_filename\n"
	quit()
newLine = f.readline()
## Acquire the Number of Diseases and Paitents
DiseaseNum, PatientNum = newLine.split()
print "Disease:", DiseaseNum, "Patient: ", PatientNum
## Naming the lists
DiseaseDictionary = dict()
DiseaseMinMaxDictionary = dict()
DiseaseSlopeDictionary = dict()
DiseaseByIndex = [] 
NumofSym = [] 
SymListByDiseaseIndex = [] ## List of Symptoms indexed by Disease number
DiseaseProbByIndex = [] ##Probability of Disease by index
SymTrue_D_True = [] ##Line 3 info
SymTrue_D_False = [] ## Line 4 info
# Output File name should be inputname_inference.txt
outputName = str(sys.argv[2])
DesFile = open(outputName.replace(".txt","_inference.txt"), 'w')
for i in range(int(DiseaseNum)):
	## First Line, Get name of disease, number of symtoms and probability.
	newLine = f.readline().split()
	DiseaseByIndex.append(newLine[0])
	NumofSym.append(int(newLine[1]))
	DiseaseProbByIndex.append(float(newLine[2]))
	##Read the second line into a list SymListByDiseaseIndex[i], indexed by Disease
	SymListByDiseaseIndex.append(eval(f.readline()))
	##Store the rest of the probability into each list
	SymTrue_D_True.append(eval(f.readline()))
	SymTrue_D_False.append(eval(f.readline()))
## Done with inputs, start calculating
for i in range(int(PatientNum)):
	## for each patient i
	print "Patient-%s:" % (i+1)
	DesFile.write("Patient-%s:\n" % (i+1))
	for j in range(int(DiseaseNum)):
		## for each disease indexed by j, read next line, calculate true & false
		patientCondition = eval(f.readline())
		## Set the Disease Probability for True | False Case
		val_Tcase = DiseaseProbByIndex[j];
		val_Fcase = 1 - DiseaseProbByIndex[j];
		max_Tcase = DiseaseProbByIndex[j];
		max_Fcase = 1 - DiseaseProbByIndex[j];
		min_Tcase = DiseaseProbByIndex[j];
		min_Fcase = 1 - DiseaseProbByIndex[j];
		## True Case
		SlopeUp = [0]
		SlopeDown = [0]
		for index, c in enumerate(patientCondition):
			if c == 'T':
				val_Tcase = val_Tcase * SymTrue_D_True[j][index]
				val_Fcase = val_Fcase * SymTrue_D_False[j][index]
				## Max case
				max_Tcase = max_Tcase * SymTrue_D_True[j][index]
				max_Fcase = max_Fcase * SymTrue_D_False[j][index]
				## Min case
				min_Tcase = min_Tcase * SymTrue_D_True[j][index]
				min_Fcase = min_Fcase * SymTrue_D_False[j][index]
			elif c == 'F':
				val_Tcase = val_Tcase * (1 - SymTrue_D_True[j][index])
				val_Fcase = val_Fcase * (1 - SymTrue_D_False[j][index])
				## Max case
				max_Tcase = max_Tcase * (1 - SymTrue_D_True[j][index])
				max_Fcase = max_Fcase * (1 - SymTrue_D_False[j][index])
				## Min case
				min_Tcase = min_Tcase * (1 - SymTrue_D_True[j][index])
				min_Fcase = min_Fcase * (1 - SymTrue_D_False[j][index])
			elif c == 'U':
				## Unknown Case, Find Max, and Min with all unknown probability
				## Test both true and false, to see which one give max
				Test_True_T = max_Tcase 
				Test_True_F = max_Fcase
				Test_False_T = max_Tcase
				Test_False_F = max_Fcase
				Test_True_T = Test_True_T * SymTrue_D_True[j][index]
				Test_True_F = Test_True_F * SymTrue_D_False[j][index]
				Test_False_T = Test_False_T * (1 - SymTrue_D_True[j][index])
				Test_False_F = Test_False_F * (1 - SymTrue_D_False[j][index])
				alpha_test_T = 1 / (Test_True_T + Test_True_F)	## True case
				alpha_test_F = 1 / (Test_False_T + Test_False_F) ## False Case
				if (alpha_test_T * Test_True_T) > (alpha_test_F * Test_False_T):
					## The test True case is higher, get max case
					max_Tcase = max_Tcase * SymTrue_D_True[j][index]
					max_Fcase = max_Fcase * SymTrue_D_False[j][index]
					## get min case
					min_Tcase = min_Tcase * (1 - SymTrue_D_True[j][index])
					min_Fcase = min_Fcase * (1 - SymTrue_D_False[j][index])
				else:
					## The False case is higher, get max case
					max_Tcase = max_Tcase * (1 - SymTrue_D_True[j][index])
					max_Fcase = max_Fcase * (1 - SymTrue_D_False[j][index])
					## get min case
					min_Tcase = min_Tcase * SymTrue_D_True[j][index]
					min_Fcase = min_Fcase * SymTrue_D_False[j][index]

		alpha = 1 / (val_Tcase + val_Fcase)
		alpha_max = 1 / (max_Tcase + max_Fcase)
		alpha_min = 1 / (min_Fcase + min_Tcase)
		for index, c in enumerate(patientCondition):
			##After calculating probability with no U
			if c == 'U':
				## Find the condition that will lead to biggest increase or decrease of probability
				##Get value without guessing unknowns
				Original_True_T = val_Tcase * SymTrue_D_True[j][index]
				Original_True_F = val_Fcase * SymTrue_D_False[j][index]
				Original_False_T = val_Tcase * (1 - SymTrue_D_True[j][index])
				Original_False_F = val_Fcase * (1 - SymTrue_D_False[j][index])
				alpha_single_case_T = 1 / (Original_True_T + Original_True_F)
				alpha_single_case_F = 1 / (Original_False_T + Original_False_F)
				P_U_True = alpha_single_case_T * Original_True_T
				P_U_False = alpha_single_case_F * Original_False_T
				P_no_U = alpha * val_Tcase
				if  P_U_True > P_no_U :
					## Assuming True will give higher probability, calculate the difference
					diff = P_U_True - P_no_U
					if (SlopeUp[0] < diff):
						SlopeUp = [diff, SymListByDiseaseIndex[j][index], 'T']
				if P_no_U > P_U_True:
					## Assuming True give lower probability
					diff = P_no_U - P_U_True
					if (SlopeDown[0] < diff):
						SlopeDown = [diff, SymListByDiseaseIndex[j][index], 'T']
				if P_U_False > P_no_U:
					diff_F = P_U_False - P_no_U
					## Assuming False gives higher porbability
					if (SlopeUp[0] < diff_F):
						SlopeUp = [diff_F, SymListByDiseaseIndex[j][index], 'F']
				if P_no_U > P_U_False:
					diff_F = P_no_U - P_U_False
					if (SlopeDown[0] < diff_F):
						SlopeDown = [diff_F, SymListByDiseaseIndex[j][index], 'F']

		## Probability of the disease gievn the symptoms
		DiseaseDictionary[DiseaseByIndex[j]] = "%0.4f" % (alpha * val_Tcase)
		DiseaseMinMaxDictionary[DiseaseByIndex[j]] = ["%0.4f" % (alpha_min * min_Tcase), "%0.4f" % (alpha_max * max_Tcase)]
		if SlopeUp[0] == 0 or SlopeDown[0] == 1:
			## No biggest increase or decrease
			DiseaseSlopeDictionary[DiseaseByIndex[j]] = ["none", 'N', "none", 'N']
		else:
			DiseaseSlopeDictionary[DiseaseByIndex[j]] = [SlopeUp[1], SlopeUp[2], SlopeDown[1], SlopeDown[2]]
	print DiseaseDictionary
	DesFile.write("%s\n" % str(DiseaseDictionary))
	print DiseaseMinMaxDictionary
	DesFile.write("%s\n" % str(DiseaseMinMaxDictionary))
	print DiseaseSlopeDictionary
	DesFile.write("%s\n" % str(DiseaseSlopeDictionary))
DesFile.close()


