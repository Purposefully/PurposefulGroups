function doGet() {
    return HtmlService.createTemplateFromFile('Index')
      .evaluate()
      .setSandboxMode(HtmlService.SandboxMode.NATIVE);
}

function processForm(formObject) {
  var cName = formObject.className;
  var sNames = formObject.classList
  console.log(sNames);
  var sList = sNames.split("\n");
  var formUrl = createForm(cName, sList);
  var template = HtmlService.createTemplateFromFile('Directions');
  template.url = formUrl
  return template.evaluate()
    .setSandboxMode(HtmlService.SandboxMode.NATIVE)
    .getContent();
}

function createForm(cName, sList) {

  // Create new form
  var form = FormApp.create('Group Preferences Form for ' + cName);
  var formUrl = form.getEditUrl();
  form.setDescription('As explained in class, this form gives me information about your experience working with different students in this class.');
  //form.setDestination(FormApp.DestinationType.SPREADSHEET, ss.getId());
  
  // Add drop-down list to select student name
  var item = form.addListItem()
  item.setTitle('Select your name from the list')
      .setChoiceValues(sList)
      .setRequired(true);
  
  // Add Section Header and directions
  var item = form.addSectionHeaderItem();
  item.setTitle('Which option best describes your experience with each person?');
  
  for (var n = 0; n < sList.length; n++){
      // Add the questions about individual classmates
      var item = form.addMultipleChoiceItem()
          .setTitle(sList[n]) // How do I get these filled in automatically?
          .setChoiceValues([
                '1 = We work really well together. We stay on task, share the work, and do quality work together.',
                "2 = We work ok together but there's room for improvement.",
                "3 = We have not worked together so I don't know how well it would go. Maybe fine, maybe not.",
                "4 = Although we can work together, it requires more effort than normal to stay on task and collaborate.",
                "5 = When we have worked together in the past, it has not gone well at all for some reason or another.",
                "This is me!"])
          .setRequired(true);
  }          
  
  // Thank you message
  var item = form.addSectionHeaderItem();
  item.setTitle('Thank you!');
  
  return formUrl;
}