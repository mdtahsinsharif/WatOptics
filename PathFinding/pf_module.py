import polygon as p

def FindStartEndTri(tIds, current, dest):
    '''
    Inputs:
    tIds: dictionary; maps triangle Ids to actual triangle
    current: (x,y) of current user location
    dest: (x,y) of user destination

    Output:
    returns (start, end) where start is the midpoint of the triangle where 'current' lies
    and end is the midpoint of the triangle where 'dest' lies
    '''

    

def FindPath(tIds, start, end):
    '''
    Inputs:
    start: midpoint of the triangle where the current location of the user lies
    end: midpoint of the triangle where the destination lies
    tIds: dictionary; maps triangle Ids to actual triangles
    
    Output:
    returns a list containing the ids of the triangles which form the fastest path
    from the start to the end
    '''