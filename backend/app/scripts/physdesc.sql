SELECT
	tt."H-ID" as text_id,
	w."H-ID" as witness_id,
	w.preferred_siglum witness_siglum,
	tt.preferred_name text_title,
	tt.language_COLUMN text_language,
	tt.literary_form text_form,
	g.preferred_name as text_genre,
	w.date_of_creation.estMinDate witness_earliest_date,
	w.date_of_creation.estMaxDate witness_latest_date,
	w.date_of_creation.value as witness_exact_or_circa_date,
	dt."H-ID" doc_id,
	dt.current_shelfmark doc_shelfmark,
	r.preferred_name doc_repository,
	p2.place_name as doc_city,
	p2.country as doc_country,
	p.div_order as part_order,
	p."H-ID" as part_id,
	pd."H-ID" as physdesc_id,
	list_aggr(p.page_ranges, 'string_agg', ',') as foliation,
	p."verses_per_line",
	p.number_of_lines,
	p.number_of_verses,
	pd.material,
	pd.form,
	pd.amount_of_illustrations,
	case when 'no decoration' in pd.has_decorations then 1 else 0 end has_no_decoration,
	case when 'unrelated pictures' in pd.has_decorations then 1 else 0 end has_pictures,
	case when 'initial' in pd.has_decorations then 1 else 0 end has_initials,
	case when 'rubrication' in pd.has_decorations then 1 else 0 end has_rubrication,
	case when 'incomplete dec.' in pd.has_decorations then 1 else 0 end has_incomplete_decoration,
	case when pd.folio_size_width like 'NA' then null else pd.folio_size_width end folio_size_width,
	case when pd.folio_size_height like 'NA' then null else pd.folio_size_height end folio_size_height,
	case when pd.folio_size_reference like 'NA' then null else pd.folio_size_reference end folio_size_reference,
	case when pd.estimated_folio_size_width like 'NA' then null else pd.estimated_folio_size_width end estimated_folio_size_width,
	case when pd.estimated_folio_size_height like 'NA' then null else pd.estimated_folio_size_height end estimated_folio_size_height,
	case when pd.estimated_folio_size_reference like 'NA' then null else pd.estimated_folio_size_reference end estimated_folio_size_reference,
	case when pd.writing_surface_area_width like 'NA' then null else pd.writing_surface_area_width end writing_surface_area_width,
	case when pd.writing_surface_area_height like 'NA' then null else pd.writing_surface_area_height end writing_surface_area_height,
	case when pd.writing_surface_area_reference like 'NA' then null else pd.writing_surface_area_reference end writing_surface_area_reference,
	pd.number_of_columns,
	pd.number_of_lines_in_writing_area,
	pd.above_top_line,
	pd.script_type,
	pd.subscript_type,
	pd.review_note
FROM main.TextTable tt
JOIN main.Genre g on tt."specific_genre H-ID" = g."H-ID"
JOIN (
	SELECT unnest(w."observed_on_pages H-ID") as pages_id, w."is_manifestation_of H-ID", w.preferred_siglum, w.date_of_creation, w."H-ID"
	FROM main.Witness w
) w on tt."H-ID" = w."is_manifestation_of H-ID"
JOIN main.Part p on w.pages_id = p."H-ID"
JOIN main.PhysDesc pd on pd."subject_of_description H-ID" = p."is_inscribed_on H-ID"
JOIN main.DocumentTable dt on pd."subject_of_description H-ID" = dt."H-ID"
JOIN main.Repository r on dt."location H-ID" = r."H-ID"
JOIN main.Place p2 on p2."H-ID" = r."city H-ID"
WHERE p."physical_description H-ID" IS NOT NULL
ORDER BY tt."H-ID", w."H-ID";
