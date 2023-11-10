(define (domain gripper-strips)
   (:predicates
		(box ?b)
		(gripper ?g)
		(free ?g)
		(on ?above ?below)
		(top ?b)
		(carry ?b ?g)
		(on_table ?b))
		
    (:functions
        (total-cost)
        (UnstackCost)
        (StackCost)
        (PickCost)
        (PlaceCost)
       )


   (:action unstack
       :parameters (?gripper ?obj_above ?obj_below)
       :precondition  (and (box ?obj_above) (box ?obj_below) (top ?obj_above)
                           (gripper ?gripper) (free ?gripper) (not (= ?obj_above ?obj_below))
                           (on ?obj_above ?obj_below))
       :effect (and (carry ?obj_above ?gripper)
		       (top ?obj_below) 
		       (not(on ?obj_above ?obj_below)) 
		       (not (top ?obj_above)) 
		       (not (free ?gripper))
		       (increase (total-cost) (UnstackCost)))
	)


   (:action stack
       :parameters  (?gripper ?obj_above ?obj_below)
       :precondition  (and (box ?obj_above) (box ?obj_below) (top ?obj_below)
                           (gripper ?gripper) (carry ?obj_above ?gripper) (not (= ?obj_above ?obj_below)))
       :effect (and (on ?obj_above ?obj_below)
                    (top ?obj_above)
                    (not (top ?obj_below))
		            (free ?gripper)
		            (not (carry ?obj_above ?gripper))
    		        (increase (total-cost) (StackCost)))
    )
		            
	(:action pick
       :parameters (?gripper ?obj)
       :precondition  (and (box ?obj) (top ?obj) (on_table ?obj)
                           (gripper ?gripper) (free ?gripper))
       :effect (and (carry ?obj ?gripper)
		       (not (top ?obj)) 
		       (not (on_table ?obj))
		       (not (free ?gripper))
   		       (increase (total-cost) (PickCost)))
		       
	)


   (:action place
       :parameters  (?gripper ?obj)
       :precondition  (and (box ?obj)
                           (gripper ?gripper) (carry ?obj ?gripper))
       :effect (and (on_table ?obj)
                    (top ?obj)
		            (free ?gripper)
		            (not (carry ?obj ?gripper))
    		        (increase (total-cost) (PlaceCost)))
		            
		            
    )
)