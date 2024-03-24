--create index for first letter of name in names
CREATE INDEX idx_name_first ON names(name(1));
