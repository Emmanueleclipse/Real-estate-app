function mortgage_set_field(field,value,type)
{
	if (type == 'price') value = numberWithCommas(Math.round(value));
	else if (type == 'percent') value = Math.round(value*100);
	$(field).val(value);
}

function mortgage_get_figures()
{
	var vars = { price : parseInt($('#price').val().replace(',','')), mortgage_percent : $("#mortgage_percent").val()/100, mortgage_amount : parseInt($("#mortgage_amount").val().replace(',','')), interest_rate : $("#interest_rate").val(), repayment_years : $("#repayment_years").val(), income : $("#income").val().replace(',','') };
	vars['total_repayment'] = compound_interest(vars);
	vars['monthly_repayments'] = Math.round(vars['total_repayment']/vars['repayment_years']/12)
	return vars;
}

function mortgage_change_price()
{
	var vars = mortgage_get_figures();
	mortgage_set_loan(vars);
	mortgage_set_income(vars);
	show_costs(vars);
}

function mortgage_change_percent()
{
	var vars = mortgage_get_figures();
	mortgage_set_field("#mortgage_amount",vars['price']*vars['mortgage_percent'], 'price')
	mortgage_set_income(vars);
	show_costs(vars);
}

function mortgage_change_rate()
{
	var vars = mortgage_get_figures();
	mortgage_set_income(vars);
	show_costs(vars);
}

function mortgage_change_years()
{
	var vars = mortgage_get_figures();
	mortgage_set_income(vars);
	show_costs(vars);
}

function mortgage_set_income(vars)
{
	mortgage_set_field("#income",vars['monthly_repayments']*3, 'price')
}

function mortgage_change_amount()
{
	var vars = mortgage_get_figures();
	if (vars['mortgage_amount'] > vars['price']*1.1) { vars['mortgage_amount'] = vars['price']*1.1; alert(vars['mortgage_amount']); mortgage_set_field('#mortgage_amount', vars['mortgage_amount'], 'price'); }
	mortgage_set_field("#mortgage_percent",vars['mortgage_amount']/vars['price'], 'percent')
	mortgage_set_income(vars);
	show_costs(vars);
}

function mortgage_change_income()
{
	var vars = mortgage_get_figures();

	vars['mortgage_amount'] = compound_reverse(vars);
	vars['price'] = Math.round(vars['mortgage_amount'] / vars['mortgage_percent']);
	mortgage_set_price(vars);
	mortgage_set_loan(vars);
	show_costs(vars);

}

function mortgage_set_loan(vars)
{
	mortgage_set_field("#mortgage_amount",vars['price']*vars['mortgage_percent'], 'price');
}

function mortgage_set_price(vars)
{
	mortgage_set_field("#price",vars['price'], 'price');
}

function calculateTotalCompoundInterest(principal, annual_rate, n_times, t_years) {
    return principal*(Math.pow(1 + annual_rate/n_times, n_times*t_years) - 1);
}

function compound_interest(vars) {
  var principal = parseFloat(vars['mortgage_amount']);
  var interestRate = parseFloat(vars['interest_rate']);
  interestRate = interestRate / 100;
  var timesCompounded = 1;
  var termOfLoan = parseFloat(vars['repayment_years']);
  var a = interestRate / timesCompounded;
  var b = 1 + a;
  var c = timesCompounded * termOfLoan;
  var d = Math.pow(b, c);
  var amount = (principal * d);
  return Math.round(amount);
}

function compound_reverse(vars) {
  var interestRate = parseFloat(vars['interest_rate']);
  interestRate = interestRate / 100;
  var timesCompounded = 1;
  var termOfLoan = parseFloat(vars['repayment_years']);
  var a = interestRate / timesCompounded;
  var b = 1 + a;
  var c = timesCompounded * termOfLoan;
  var d = Math.pow(b, c);
  var totalpaid = parseFloat(vars['income'])/3*12*c;
  var amount = (totalpaid / d);
  return Math.round(amount);
}

function max_loan(vars)
{
	var monthly_repayments = vars['income'] / 3;
	var payments = vars['repayment_years']*12;
	var monthly_interest = vars['interest_rate']/100/12;
	var t = Math.pow(1+monthly_interest,payments);
	var mortgage_amount = monthly_repayments / ((monthly_interest * t) / (t - 1));
	return Math.round(mortgage_amount);
}

function init_costs()
{
	var vars = {};
	vars['price'] = getQueryStringValue('price')!=''?parseInt(getQueryStringValue('price')):250000; mortgage_set_price(vars);
    vars['mortgage_percent'] = (getQueryStringValue('mortgage_percent')!=''?parseInt(getQueryStringValue('mortgage_percent')):80); mortgage_set_field('#mortgage_percent',vars['mortgage_percent'],'integer');
    vars['mortgage_percent'] = vars['mortgage_percent'] /100;
    vars['interest_rate'] = getQueryStringValue('interest_rate')!=''?parseInt(getQueryStringValue('interest_rate')):1.4;; mortgage_set_field('#interest_rate',vars['interest_rate'],'float');
    vars['repayment_years'] = getQueryStringValue('repayment_years')!=''?parseInt(getQueryStringValue('repayment_years')):25; mortgage_set_field('#repayment_years',vars['repayment_years'],'integer');
    vars['mortgage_amount'] = vars['price']*(vars['mortgage_percent']); mortgage_set_loan(vars);

	vars['total_repayment'] = compound_interest(vars);
	vars['monthly_repayments'] = Math.round(vars['total_repayment']/vars['repayment_years']/12);

	mortgage_set_income(vars);

	show_costs(vars);
}

function show_costs(vars)
{
	var calc_price = vars['price'];
	var calc_interest = compound_interest(vars);
	var calc_mortgage = vars['mortgage_amount'];

	var calc_notaire = Math.round(calc_price * 0.078);
	var calc_loantax = Math.round(250 + calc_mortgage / 1666 + (192+(calc_mortgage-30000)*0.0028*1.2));
	var calc_total_costs = calc_notaire + calc_loantax;
	var calc_cash = calc_price + calc_total_costs - calc_mortgage;

	$('#summary_price').html(showPrice(calc_price));
	$('#summary_repayments').html(showPrice(vars['monthly_repayments']));
	$('#summary_cash').html(showPrice(calc_cash));
	$('#summary_total').html(showPrice(calc_price+calc_total_costs));
	$('#summary_interest').html(showPrice(calc_interest-calc_mortgage));

	$('#cost_notaire').html(showPrice(calc_notaire));
	$('#cost_loan').html(showPrice(calc_loantax));

}
