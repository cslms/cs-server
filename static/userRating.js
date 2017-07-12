$(function () {
 
  $(".cs-sparta__rateYo").each(function() {
    $(this).rateYo({
      starWidth: "20px",
      rating: $(this)[0].id.split('-')[2],
      halfStar: true
    })
    $(this).on('click', function() {
      userId = $(this)[0].id.split('-')[1];
      rating = $(this).rateYo('option', 'rating');
      $.ajax('/sparta/membersrating', {
        method: 'POST',
        data: {
          'user_evaluated': userId,
          'rating': rating
        },
        statusCode: {
          201: function() {
            amount_div = $('#RLen-'+userId)
            students_amount = amount_div.html().split(' ')[0]
            new_amount = parseInt(students_amount) + 1
            amount_div.html(new_amount + ' ' + amount_div.html().split(' ')[1])
          }
        }
      })
    })
  });
})




"12232321123 alunos"
split(' ')