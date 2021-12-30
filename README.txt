            _                     
           | |                    
  _ __   __| | __ _   _ __  _   _ 
 | '_ \ / _` |/ _` | | '_ \| | | |
 | |_) | (_| | (_| |_| |_) | |_| |
 | .__/ \__,_|\__,_(_) .__/ \__, |
 | |                 | |     __/ |
 |_|                 |_|    |___/ 

What is pda.py?
pda.py contains a python library to implement deterministic pushdown automata and nondeterministic pushdown automata as a standalone program or can be imported into other python libraries.

How do I run pda.py?
You can pda.py in a terminal with a given text (*.txt) file representing the automaton. Then you will be prompted to input a word or sentence until Ctrl + c is pressed. If no file is found or if given an incorrect file format the program may fail to load.

An example of starting pda.py as a standalone program.

	> python pda.py dpda1.txt
	< Looking for dpda1.txt
	< dpda1.txt Found!
	> Please input a word: 

The program shall output the results as either 'Accepted' meaning the word exists in the language described by the automaton or 'Rejected' meaning the word does not exist in the language described by the automaton. Regardless, of whether the word is 'Accepted' or 'Rejected', the program will output the path, transitions, and stack.

A DPDA representing the language 0^n 1^n:

	> python automatons.py dpda1.txt
	< Looking for dpda1.txt
	< dpda1.txt Found!
	> Please input a word: 000111
	> String Accepted. Path:
	> Q0 Q1 Q1 Q1 Q1 Q2 Q2 Q2 Q3
	> 
	> Transitions taken:
	>  0 0 0 1 1 1 
	>
	> Stack:
	> 

What does a file look like?
The main difference between DPDA and PDA files beside the architecture and behaviour is the first line of the file shall specify either 'DPDA' or 'PDA':
- The first line is 'DPDA' or 'PDA'
- The second line is the alphabet (sigma) where each char is separated by a space.
- The third line is the stack alphabet (gamma) where each char is separated by a space
- The fourth line is the amount of states in the automaton
- The fifth line is optional if there no accept states, if there are accept states then each of the states should be prefixed by a 'Q' followed by the state number. Each accept state should be separated by a space.
- The next line should be three consecutive dashes '---'.
- The following lines will indicate a rule on each line, where each rule is in five parts separated by spaces. Parts one and four are prefixed with 'Q' followed by the state number, which represent the in and out states, respectively. The second part of the rule is a single char transition the in state uses to get to the out state. The third part of rule is the stack character to pop. The sixth part of the rule is the character to push onto the stack.

DPDA file example:

	DPDA
	0 1
	$ 0
	5
	Q3
	---
	Q0     Q1 $
	Q1 0   Q1 0
	Q1 1 $ Q4  
	Q1 1 0 Q2  
	Q2 1 0 Q2  
	Q2   $ Q3  
	Q2 0 0 Q4  
	Q3 0   Q4  
	Q3 1   Q4  
	Q4 0   Q4  
	Q4 1   Q4  


PDA file example:
	PDA
	a b c
	$ a
	7
	Q3 Q6
	---
	Q0     Q1 $
	Q1 a   Q1 a
	Q1     Q2  
	Q1     Q4  
	Q2 b a Q2  
	Q2   $ Q3  
	Q3 c   Q3  
	Q4 b   Q4  
	Q4     Q5  
	Q5 c a Q5  
	Q5   $ Q6  
