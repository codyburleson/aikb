
```dataviewjs
const today = DateTime.now();
dv.table(["Name","Start Date", "End Date"],
	dv.pages('"3 Resources/Events/Cancelled Events"')
    	.sort(doc => [ doc.endDate ], 'asc')
		.where(doc => 
			doc.file.name != "Cancelled Events"
		)
		.map(doc => 
			[
				doc.file.link,
				doc.startDate,
				doc.endDate,
			])		
    )
```
