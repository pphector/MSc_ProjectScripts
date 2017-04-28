#!/usr/bin/python

"""
A set of tools to handle Seeder motifs. Based on a new class called SeederMotif.
Useful for parsing and manipulating the information obtained from running Seeder. 
"""

from sys import argv
import re

class SeederMotif(object): 
    ''' A type of motif class that contains all the information of a seeder motif'''

    def __init__(self, number, width, seedwidth, pvalue, qvalue, time):
        '''
        Create a SeederMotif instance.
        SeederMotifs must be created with the following arguments, in this order: 
         - IDnumber: Just for ID purposes, it shouldn't be used for math operations, string
         - Width : The width of the motif, integer
         - Seedwidth: The seed width used to predict the motif, integer
         - P-value: As calculated by seeder, float (can be in the form '1e-10')
         - Q-value: As calculated by seeder, float (can be in the form '1e-10')
         - Time: Time it took to predict the motif in seconds, integer
        '''
        self.origin = None #This will contain the information on the subgroup for ID purposes
        self.number = str(number)
        self.width = int(width) 
        self.seedwidth = int(seedwidth) 
        self.pvalue = float(pvalue) 
        self.qvalue = float(qvalue) 
        self.time = int(time)

    def setNFM(self, matrix):
        '''
        Define a NFM matrix from the text in a Seeder output file.
        Requires one argument: The matrix text from the seeder output file. 
        This text must contain the following structure: 
            - The first line, starting with the following string '>NFM' and the Motif number
            - A <BLANKLINE>
            - A line with the Nucleotide letters in the following order ACGT
            - One line per motif position, starting with the string 'P#' where # is the motif position number
            - A final <BLANKLINE>
              Each of these lines has 4 numbers which correspond to the frequency of each nucleotide in the motif. 
        '''
        #Define the dictionary that will contain the matrix information
        NFM = []

        #Verify that the number of lines in the input text is the appropriate
        if matrix.count('\n') != (self.width + 3):
            raise ValueError('There is a problem with the input text: incorrect number of lines')

        #First split the text matrix into lines and keep only the information containing lines
        lines = matrix.split('\n')[3:-1]
        #Now split the lines into of position numbers using the re module
        #And append info into NFM
        for line in lines:
            #Create empty temporary dictionary
            tNFM = {}
            #Fill with information found in the line
            tNFM['A'] = float(re.split(r'\s+',line)[1])
            tNFM['C'] = float(re.split(r'\s+',line)[2])
            tNFM['G'] = float(re.split(r'\s+',line)[3])
            tNFM['T'] = float(re.split(r'\s+',line)[4])
            #Add the line info into the final NFM matrix
            NFM.append(tNFM)

        self.nfm = NFM

    def setPWM(self, matrix):
        '''
        Define a PWM matrix from the text in a Seeder output file. 
        Requires one argument: The matrix text from the seeder output file. 
        This text must contain the following structure: 
            - The first line, starting with the following string '>PWM' and the Motif number
            - A <BLANKLINE>
            - A line with the Nucleotide letters in the following order ACGT
            - One line per motif position, starting with the string 'P#' where # is the motif position number
            - A final <BLANKLINE>
              Each of these lines has 4 numbers which correspond to the frequency of each nucleotide in the motif. 
        '''
        #Define the dictionary that will contain the matrix information
        PWM = []

        #Verify that the number of lines in the input text is the appropriate
        if matrix.count('\n') != (self.width + 3):
            raise ValueError('There is a problem with the input text: incorrect number of lines')

        #First split the text matrix into lines and keep only the information containing lines
        lines = matrix.split('\n')[3:-1]
        #Now split the lines into of position numbers using the re module
        #And append info into PWM
        for line in lines:
            #Create empty temporary dictionary
            tPWM = {}
            #Fill with information found in the line
            tPWM['A'] = float(re.split(r'\s+',line)[1])
            tPWM['C'] = float(re.split(r'\s+',line)[2])
            tPWM['G'] = float(re.split(r'\s+',line)[3])
            tPWM['T'] = float(re.split(r'\s+',line)[4])
            #Add the line info into the final PWM matrix
            PWM.append(tPWM)

        self.pwm = PWM

    def stdmatrix(self, mattype):
        '''
        Returns a standard representation of a PWM or NFM matrix, based on the requirements of other motif parsers. 
        Requires that the matrix which will be returned is already defined using methods setPWM() or setNFM().
        Requires one argument: 
        - (mattype) Type of matrix: a string specifying the type of matrix that is expected. Can be 'nfm' or 'pwm'
        '''
        #Make sure input is in all caps
        mattype = mattype.upper()

        #Select template based on the type of matrix requested
        if mattype == 'NFM':
            try:
                template = self.nfm
            except AttributeError: 
                return 'ERROR: No NFM defined. Please use the setNFM() method to define a NFM for this motif'
        elif mattype == 'PWM':
            try:
                template = self.pwm
            except AttributeError:
                return 'ERROR: No PWM defined. Please use the setPWM() method to define a PWM for this motif'
        else :
            raise ValueError('Incorrect or unsupported type')

        #Define output variable
        output = '#'

        #Create first row, with only position numbers
        for num in range(self.width):
            output += '\t'+str(num)

        #Build rest of matrix, row by row        
        for base in ['A','C','G','T']:
            #Create new row for new base
            output += '\n#'+ base

            #Fill out values for that row in each position
            for num in range(self.width):
                output += '\t'+ str(round(template[num][base],3))

        return output

    def stampmatrix(self, mattype):
        '''
        Returns a Lx4 matrix representation of the motif based on the format used by STAMP. 
        It contains a heading starting with '>'. 
        Requires that the matrix which will be returned is already defined using methods setPWM() or setNFM().
        Requires one argument:
        - (mattype) Type of matrix: a string specifying the type of matrix that is expected. Can be 'nfm' or 'pwm'
        '''

        #Make sure input is in all caps
        mattype = mattype.upper()

        #Select template based on the type of matrix requested
        if mattype == 'NFM':
            try:
                template = self.nfm
            except AttributeError: 
                return 'ERROR: No NFM defined. Please use the setNFM() method to define a NFM for this motif'
        elif mattype == 'PWM':
            try:
                template = self.pwm
            except AttributeError:
                return 'ERROR: No PWM defined. Please use the setPWM() method to define a PWM for this motif'
        else :
            raise ValueError('Incorrect or unsupported type')

        #Create header with motif number
        output = '>Motif ' + self.number 

        #Fill out values for that row in each position
        for num in range(self.width):
        #Build rest of matrix, row by row        
            output += '\n'

            for base in ['A','C','G','T']:
                output += str(int(template[num][base])) + ' '

        return output

#PARSER FOR SEEDER FILES

#Define starline for easy identification of sections separation in seeder file
starline = '******************************************************************************\n'

#Scanner for seeder files
def seeder_parser(fileinput,significance):
    '''
    Scanner function of parser that reads the target file one line at a time.
    Has 2 arguments: 
        - fileinput : a text file object that contains the result of a seeder run. 
        - significance : float with the desired significance cutoff used for motifs. 
    Returns a list of significant motifs found in the seeder file. 
    '''
   #Create list where motifs will be saved    
    motif = []
    significance = float(significance)

    try:
        #Scanner will read motif header line by line
        line = fileinput.readline()
        #While there are lines to read, it will try to find a header
        while line != None:
            #If it detects a header, it will call the header consumer
            if line == starline:
                motifcandidate = seeder_header(fileinput,significance)
                if motifcandidate != None:
                    motif.append(motifcandidate)
                else:
                    return motif
            #If it can't find a header, it will keep reading the file
            else:
                line = fileinput.readline()
    except ValueError:
        #If the file is already closed, return any found motifs
        return motif    

    #If the file finishes reading without closing, close the file and return motifs
    fileinput.close()    
    return motif
    
#Consumer for seeder headers
def seeder_header(fileinput,significance):
    '''
    Handler function when scanner finds a seeder header. 
    Has 2 arguments:
        - fileinput : same text file used in the scanner, on the same line as scanner. 
        - significance : float with the desired significance cutoff used for motifs. 
    '''
    #Save header into temporary variable
    header = []
    for num in range(5):
        header.append(fileinput.readline())

    #Determine wether or not the motif is significant based on the q-value
    if fileinput.readline() == starline: 
        qvalue = float(header[3].split()[-1])

        #If motif is significant, begin parsing process      
        if qvalue < significance:
            #Call the significant motif consumer
            motif = seeder_significant(header,qvalue,fileinput) 
            return motif   
        else: 
            #Close file. There are no other significant motifs in this file.
            fileinput.close() 
            
    #If the motif header doesn't follow the seeder convention, raise an exception
    else: 
        raise ValueError('Something is wrong with the header of this seeder file. Please verify it is correct')

#Consumer for seeder-signfificant motifs
def seeder_significant(header,qvalue,fileinput):
    '''
    Handler function when scanner finds a significant motif. 
    Has 3 argumetns:
        - header : five lines of header content obtained from the seeder file
        - qvalue : already parsed q-value used to determine significance of motif
        - fileinput: same as used by header handler, used to otbain rest of information
    '''
    #Generate initial values
    initvalues = header[0].split(',')
    motifnum = initvalues[0].split()[-1]
    width = initvalues[1].split()[-1]
    seedwidth = initvalues[2].split()[-1]
    pvalue = float(header[2].split()[-1])

    line = ''    

    #Stop when 'Time' line is reached
    while not line.startswith('Time'):
        line = fileinput.readline()
        #Parse NFM matrix
        if line.startswith('>NFM'):
            NFM = line 
            for num in range(int(width) + 2):
                NFM += fileinput.readline()
        #Parse PWM matrix    
        elif line.startswith('>PWM'):
            PWM = line
            for num in range(int(width) + 2):
                PWM += fileinput.readline()
        #Parse time
        elif line.startswith('Time'):
            time = line.split()[1]

    #Create SeederMotif instance
    motif = SeederMotif(motifnum,width,seedwidth,pvalue,qvalue,time)
    motif.setNFM(NFM)
    motif.setPWM(PWM)

    #Skip the three lines after the Time line to parse the rest of the file
    for num in range(3):
        line = fileinput.readline()

    #Return significant results to header, who will return to scanner
    return motif

