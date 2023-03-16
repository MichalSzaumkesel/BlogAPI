from typing import Optional

from fastapi import status, HTTPException, Response, Depends, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func

from app import models, schemas, oauth2
from app.database import get_db

router = APIRouter(prefix='/posts', tags=['Posts'])


@router.get('/', response_model=list[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("SELECT * FROM posts ORDER BY id;")
    # posts = cursor.fetchall()

    # SELECT posts.id, title, author_id, count(user_id) AS votes
    # FROM posts LEFT JOIN votes ON posts.id = votes.post_id GROUP BY posts.id;
    # noinspection PyTypeChecker
    posts = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True).group_by(models.Post.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()      # similar to db.refresh()
    # conn.commit()

    # converting the pydantic schema to dictionary and unpacking it to meet parameters of a Post model
    print(current_user)
    # models.Post.author_id = current_user.id
    new_post = models.Post(**post.dict(), author_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)  # returns added object and stores it in 'new_post' variable

    return new_post


@router.get('/{int: post_id}', response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("SELECT * FROM posts WHERE id = %s;", (str(post_id),))
    # post = cursor.fetchone()

    # noinspection PyTypeChecker
    post = db.query(models.Post, func.count(models.Vote.user_id).label('votes')).\
        join(models.Vote, models.Post.id == models.Vote.post_id, isouter=True)\
        .group_by(models.Post.id).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return post


@router.delete('/{int: post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("DELETE FROM posts WHERE id = %s RETURNING *;", (str(post_id),))
    # deleted_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == post_id)  # this is just a query; no row returned

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {post_id} does not exist')

    if post_query.first().author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot delete other user's post")
    else:
        db.delete(post_query.first())
        # post.delete(synchronize_session=False)    # alternative way
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put('/{int: post_id}', response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user=Depends(oauth2.get_current_user)):
    # cursor.execute("UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;",
    #                (post.title, post.content, post.published, str(post_id)))
    # updated_post = cursor.fetchone()

    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if post_query.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Post with id: {post_id} does not exist')

    if post_query.first().author_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot update other user's post")
    else:
        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
    return post_query.first()
