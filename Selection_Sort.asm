# Copying begins
# Here, we copy the array from one memory location to another
addi $s0,$zero,0               
#initializing the loop counter variable
addi $t4,$t2,0                  
                               
addi $t5,$t3,0                  
              
#loop begins and runs until value in $s0 becomes equal to value in $t1
ForLoopCopy: beq $s0,$t1,exitForLoopCopy  
             
            #performing operations intended in the loop-copying the elements of the array to another location
             lw $t6,0($t4)
             sw $t6,0($t5)
            
             addi $t4,$t4,4
             addi $t5,$t5,4
             addi $s0,$s0,1                
             #jumping back to the beginning of the loop
             j ForLoopCopy                 
             
# exitForLoopCopy:
# Copying ends

#sorting begins

#exit instruction for the loop
exitForLoopCopy: addi $s0,$zero,0
#assigning 0 to the value stored at $s0               
addi $t4,$t1,-1            
#outer loop for sorting begins     
OuterLoop :  beq $s0,$t4,exitOuterLoop 
            #exit condition for the loop is when the counter variable becomes equal to the number of elements in the array - 1        
             # $s1 = min_index , $s2 = j
             addi $s1,$s0,0     
             addi $s2,$s0,1     
             addi $t5,$t3,0     
             #inner loop for sorting begins
             InnerLoop :  beq $s2,$t1,exitInnerLoop  
             #exit condition for the loop is when the counter variable equals number of elements in the array
             		   		# $s4 = j*4+t3
                            #sorting mechanism begins
             		      addi $s4,$0,4 
             		      mul $s4,$s4,$s2  
             		      add $s4,$s4,$t3  
             		   		# $s5 = minindex($s1)*4 + t3
						  addi $s5,$0,4 
             		      mul $s5,$s5,$s1  
             		      add $s5,$s5,$t3  


                          lw $t7,0($s4) 
                          lw $t8,0($s5) 
                          slt $t9,$t7,$t8  
						  addi $s3,$0,1
                          beq $t9,$s3,ChangeMinIndex
                          #updating the index of minimum element
                          addi $s2,$s2,1 
                          j InnerLoop
                          ChangeMinIndex : addi $s1,$s2,0 
                          addi $s2,$s2,1 
                          j InnerLoop
                          #jumping back to the inner loop beginning

             exitInnerLoop: 		addi $s6,$0,4 
             		      			mul $s6,$s6,$s0  
             		      			add $s6,$s6,$t3  
                            		lw $s3,0($s6)	
									addi $s5,$0,4 
             		      			mul $s5,$s5,$s1  
             		      			add $s5,$s5,$t3  
									lw $t8,0($s5) 
                            		sw $s3,0($s5)	
                            		sw $t8,0($s6)	
                            		addi $s0,$s0,1           
                            		j OuterLoop 	
                                    #jumping to the outerloop on exiting inner loop	



exitOuterLoop:
#sorting ends
#code ends