-- ============================================================================
-- SQL PRACTICE GUIDE: Chronotype Explorer Database
-- ============================================================================
-- Database: chronotype_explorer.db
-- Tables: 7 relational tables
-- Goal: Learn SQL while exploring circadian research data
-- ============================================================================

-- ----------------------------------------------------------------------------
-- LEVEL 1: BASIC SELECTS (Start here if you've never used SQL)
-- ----------------------------------------------------------------------------

-- Q1: See all participants
SELECT * FROM participants LIMIT 10;

-- Q2: Count total participants
SELECT COUNT(*) AS total_participants FROM participants;

-- Q3: See only women who work remotely
SELECT * FROM participants 
WHERE sex = 'F' AND work_modality = 'remote';

-- Q4: Average age by work modality
SELECT work_modality, ROUND(AVG(age), 1) AS avg_age
FROM participants
GROUP BY work_modality;

-- ----------------------------------------------------------------------------
-- LEVEL 2: JOINS (Combine tables to answer research questions)
-- ----------------------------------------------------------------------------

-- Q5: Join participants with their chronotype scores
SELECT 
    p.participant_id,
    p.age,
    p.sex,
    p.work_modality,
    c.meq_score,
    c.chronotype
FROM participants p
JOIN chronotype_assessments c ON p.participant_id = c.participant_id
LIMIT 10;

-- Q6: Full profile: demographics + sleep + productivity
SELECT 
    p.participant_id,
    p.age,
    p.work_modality,
    c.chronotype,
    s.social_jetlag_hours,
    pr.productivity_score
FROM participants p
JOIN chronotype_assessments c ON p.participant_id = c.participant_id
JOIN sleep_schedules s ON p.participant_id = s.participant_id
JOIN productivity_outcomes pr ON p.participant_id = pr.participant_id
WHERE p.work_modality = 'remote'
ORDER BY pr.productivity_score DESC
LIMIT 15;

-- ----------------------------------------------------------------------------
-- LEVEL 3: AGGREGATION & ANALYSIS (Answer research questions)
-- ----------------------------------------------------------------------------

-- Q7: Average productivity by chronotype category
SELECT 
    c.chronotype,
    COUNT(*) AS n,
    ROUND(AVG(pr.productivity_score), 2) AS avg_productivity,
    ROUND(AVG(s.social_jetlag_hours), 2) AS avg_social_jetlag
FROM participants p
JOIN chronotype_assessments c ON p.participant_id = c.participant_id
JOIN sleep_schedules s ON p.participant_id = s.participant_id
JOIN productivity_outcomes pr ON p.participant_id = pr.participant_id
GROUP BY c.chronotype
ORDER BY avg_productivity DESC;

-- Q8: Does work modality affect social jetlag?
SELECT 
    p.work_modality,
    COUNT(*) AS n,
    ROUND(AVG(s.social_jetlag_hours), 2) AS avg_sjl,
    ROUND(AVG(pr.productivity_score), 2) AS avg_productivity,
    ROUND(AVG(pr.procrastination_score), 2) AS avg_procrastination
FROM participants p
JOIN sleep_schedules s ON p.participant_id = s.participant_id
JOIN productivity_outcomes pr ON p.participant_id = pr.participant_id
GROUP BY p.work_modality
ORDER BY avg_sjl DESC;

-- Q9: Correlation proxy — high vs low social jetlag
SELECT 
    CASE 
        WHEN s.social_jetlag_hours < 0.6 THEN 'Low SJL (<0.6h)'
        WHEN s.social_jetlag_hours BETWEEN 0.6 AND 1.2 THEN 'Medium SJL (0.6-1.2h)'
        ELSE 'High SJL (>1.2h)'
    END AS sjl_category,
    COUNT(*) AS n,
    ROUND(AVG(pr.productivity_score), 2) AS avg_productivity,
    ROUND(AVG(pr.procrastination_score), 2) AS avg_procrastination
FROM sleep_schedules s
JOIN productivity_outcomes pr ON s.participant_id = pr.participant_id
GROUP BY sjl_category
ORDER BY avg_productivity DESC;

-- ----------------------------------------------------------------------------
-- LEVEL 4: SUBQUERIES & ADVANCED
-- ----------------------------------------------------------------------------

-- Q10: Find participants with above-average productivity for their chronotype
SELECT 
    p.participant_id,
    c.chronotype,
    pr.productivity_score,
    avg_chrono.avg_prod AS chronotype_average,
    ROUND(pr.productivity_score - avg_chrono.avg_prod, 2) AS above_average
FROM participants p
JOIN chronotype_assessments c ON p.participant_id = c.participant_id
JOIN productivity_outcomes pr ON p.participant_id = pr.participant_id
JOIN (
    SELECT chronotype, AVG(productivity_score) AS avg_prod
    FROM chronotype_assessments ca
    JOIN productivity_outcomes po ON ca.participant_id = po.participant_id
    GROUP BY chronotype
) avg_chrono ON c.chronotype = avg_chrono.chronotype
WHERE pr.productivity_score > avg_chrono.avg_prod
ORDER BY above_average DESC
LIMIT 20;

-- Q11: Lookup table JOIN — get readable names
SELECT 
    p.participant_id,
    w.modality_name,
    cr.meq_range,
    pr.productivity_score
FROM participants p
JOIN work_modality_reference w ON p.work_modality = w.modality_code
JOIN chronotype_assessments c ON p.participant_id = c.participant_id
JOIN chronotype_reference cr ON c.chronotype = cr.chronotype_code
JOIN productivity_outcomes pr ON p.participant_id = pr.participant_id
LIMIT 10;
