use test_db;
CREATE TABLE communities (
    `id` INT NOT NULL AUTO_INCREMENT,
    `community` VARCHAR(25),
    PRIMARY KEY (`id`)
);
CREATE TABLE users (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user` VARCHAR(25),
    `community` INT NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`community`)
        REFERENCES communities(`id`)
        ON DELETE CASCADE
);
CREATE TABLE posts (
    `id` INT NOT NULL UNIQUE,
    `uuid` VARCHAR(12) NOT NULL UNIQUE,
    `preview` VARCHAR(255),
    `is_locked` BOOLEAN NOT NULL,
    `is_twitter` BOOLEAN NOT NULL,
    `tweet_id` VARCHAR(50),
    `sticky_comment` INT NOT NULL,
    `link` VARCHAR(255),
    `domain` VARCHAR(255),
    `author_flair_class` VARCHAR(200),
    `is_video_mp4` BOOLEAN NOT NULL,
    `is_removed` BOOLEAN NOT NULL,
    `title` TEXT,
    `type` VARCHAR(10) NOT NULL,
    `content` TEXT,
    `score_up` INT NOT NULL,
    `score_down` INT NOT NULL,
    `score` INT NOT NULL,
    `author_flair_text` VARCHAR(255),
    `is_admin` BOOLEAN NOT NULL,
    `suggested_sort` INT NOT NULL,
    `is_stickied` BOOLEAN NOT NULL,
    `is_nsfw` BOOLEAN NOT NULL,
    `post_flair_class` VARCHAR(50),
    `is_deleted` BOOLEAN NOT NULL,
    `is_image` BOOLEAN NOT NULL,
    `comments` INT,
    `author` INT NOT NULL,
    `created` BIGINT NOT NULL,
    `is_edited` BOOLEAN NOT NULL,
    `community` INT NOT NULL,
    `is_moderator` BOOLEAN NOT NULL,
    `is_video` BOOLEAN NOT NULL,
    `video_link` VARCHAR(255),
    `is_new_user` BOOLEAN NOT NULL,
    `vote_state` INT NOT NULL,
    `post_flair_text` VARCHAR(50),
    `crosspost_uuid` VARCHAR(10),
    `is_crosspost` BOOLEAN NOT NULL,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`author`)
        REFERENCES users(`id`)
        ON DELETE CASCADE,
    FOREIGN KEY (`last_comment_author`)
        REFERENCES users(`id`)
        ON DELETE CASCADE,
    FOREIGN KEY (`community`)
        REFERENCES communities(`id`)
        ON DELETE CASCADE
);
CREATE TABLE comments (
    `id` INT NOT NULL UNIQUE,
    `uuid` VARCHAR(12) NOT NULL UNIQUE,
    `parent_id` INT NOT NULL,
    `is_removed` BOOLEAN NOT NULL,
    `content` TEXT,
    `score_up` INT NOT NULL,
    `score_down` INT NOT NULL,
    `score` INT NOT NULL,
    `is_admin` BOOLEAN NOT NULL,
    `is_stickied` BOOLEAN NOT NULL,
    `is_deleted` BOOLEAN NOT NULL,
    `author` INT NOT NULL,
    `created` BIGINT NOT NULL,
    `comment_parent_id` INT,
    `is_edited` BOOLEAN NOT NULL,
    `community` INT NOT NULL,
    `is_moderator` BOOLEAN NOT NULL,
    `is_new_user` BOOLEAN NOT NULL,
    `vote_state` INT NOT NULL,
    PRIMARY KEY (`id`),
    INDEX (`parent_id`),
    INDEX (`comment_parent_id`),
    FOREIGN KEY (`author`)
        REFERENCES users(`id`)
        ON DELETE CASCADE,
    FOREIGN KEY (`parent_id`)
        REFERENCES posts(`id`)
        ON DELETE CASCADE,
    FOREIGN KEY (`community`)
        REFERENCES communities(`id`)
        ON DELETE CASCADE
);
