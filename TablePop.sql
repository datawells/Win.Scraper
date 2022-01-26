CREATE TABLE users (
    id MEDIUMINT NOT NULL AUTO_INCREMENT,
    user VARCHAR(25),
    PRIMARY KEY (id)
)
CREATE TABLE posts (
    id INT NOT NULL UNIQUE,
    uuid VARCHAR(10) NOT NULL UNIQUE,
    preview varchar(65535),
    is_locked BOOLEAN,
    tweet_id VARCHAR(50),
    sticky_comment INT,
    link varchar(65535),
    author_flair_class VARCHAR(200),
    is_video_mp4 BOOLEAN,
    is_removed BOOLEAN,
    title VARCHAR,
    type VARCHAR(10),
    last_comment_created INT,
    content TEXT,
    score_down INT,
    author_flair_text VARCHAR(65535),
    is_twitter BOOLEAN,
    is_admin BOOLEAN,
    score INT,
    suggested_sort INT,
    is_stickied BOOLEAN,
    is_nsfw BOOLEAN,
    post_flair_class VARCHAR(50),
    is_deleted BOOLEAN,
    is_image BOOLEAN,
    comments INT,
    author INT,
    created INT,
    score_up INT,
    is_edited BOOLEAN,
    community VARCHAR(25),
    is_moderator BOOLEAN,
    last_comment_author INT,
    is_video BOOLEAN,
    video_link varchar(65535),
    is_new_user BOOLEAN,
    vote_state INT,
    domain VARCHAR(255),
    post_flair_text VARCHAR(50),
    is_crosspost BOOLEAN,
    PRIMARY KEY (id)
    FOREIGN KEY (author)
        REFERENCES users(id)
        ON DELETE CASCADE
    FOREIGN KEY (last_comment_author)
        REFERENCES users(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE TABLE comments (
    id INT NOT NULL UNIQUE,
    uuid VARCHAR(10) NOT NULL UNIQUE,
    parent_id INT NOT NULL,
    post_uuid VARCHAR(10) NOT NULL,
    is_removed BOOLEAN,
    content TEXT,
    score_down INT,
    is_admin BOOLEAN,
    score INT,
    is_stickied BOOLEAN,
    is_deleted BOOLEAN,
    author INT,
    created INT,
    score_up INT,
    comment_parent_id INT,
    is_edited BOOLEAN,
    community VARCHAR,
    is_moderator BOOLEAN,
    is_new_user BOOLEAN,
    vote_state INT,
    PRIMARY KEY (id)
    INDEX par_ind (parent_id,post_uuid),
    INDEX (comment_parent_id)
    FOREIGN KEY (author)
        REFERENCES Users(id)
        ON DELETE CASCADE
    FOREIGN KEY (parent_id)
        REFERENCES posts(id)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE utf8mb4_unicode_ci;
GO