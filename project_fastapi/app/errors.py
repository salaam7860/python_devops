# Check if post is not found and raise HTTPException 
def post_not_found(post, id):
       if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Post with id {id} was not found") 
    