-- Seed staging/test data: sample tasks for Mon (1) through Sun (7)
-- Run after schema.sql

INSERT INTO tasks (day_of_week, title, completed) VALUES
(1, 'Review weekly goals', FALSE),
(1, 'Team standup', TRUE),
(2, 'Implement feature X', FALSE),
(2, 'Code review', FALSE),
(3, 'Sprint planning', FALSE),
(4, 'Documentation update', FALSE),
(4, 'Deploy to staging', FALSE),
(5, 'Retrospective', FALSE),
(5, 'Weekly report', FALSE),
(6, 'Weekend errands', FALSE),
(6, 'Rest and recharge', FALSE),
(7, 'Plan next week', FALSE),
(7, 'Weekly review', FALSE);
