
```dataviewjs
const today = DateTime.now();
dv.table(["Name","Start Date", "End Date"],
	dv.pages()
    	.sort(doc => [ doc.endDate ], 'asc')
		.where(doc => 
			doc.file.name != "Template - Event" &&
			doc.template?.path?.includes("Template - Event")
		)
		.where(doc => doc.endDate && doc.endDate < dv.date(today))
		.map(doc => 
			[
				doc.file.link,
				doc.startDate,
				doc.endDate,
			])		
    )
```
