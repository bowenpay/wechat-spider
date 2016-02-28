$.validator.setDefaults({
  highlight: function(element) {
      $(element).closest('.form-group').addClass('has-error');
  },
  unhighlight: function(element) {
      $(element).closest('.form-group').removeClass('has-error');
  },
  errorElement: 'span',
  errorClass: 'help-block',
  errorPlacement: function(error, element) {
      if(element.parent('.input-group').length) {
          error.insertAfter(element.parent());
      } else if(element.parent('div').length){
          element.parent('div').append(error);
      } else {
          error.insertAfter(element);
      }
  }
});
$.validator.addMethod("currency_value", function(value, element) {
    return this.optional(element) || /^\d+(\.\d{1,2})?$/i.test(value);
}, "不能超过两位小数");