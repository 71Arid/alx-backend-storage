-- creates indx of name and score from names
CREATE INDEX idx_name_first_score ON names(name(1), score);
