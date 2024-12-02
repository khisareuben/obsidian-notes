
Tables is a little bit complicated so i just do it with a code

tr is used for table raws
td mean table data cells / column
th is used for table headers
thead means table heading
tbody is where the contents are placed in 
tfoot is for the last row of your table e.g totals

```
<table>

	<thead>
	
		<tr>
		
			<th>Payee</th>
			
			<th>Amount</th>
			
			<th>Date</th>
			
			<th>Status</th>
		
		</tr>
	
	</thead>

  

<tbody>

	<tr>
	
		<td>
		
			<b>John Wick</b> <br>
			
			Shoota Inc
		
		</td>
		
		<td>ksh 50,000,000</td>
		
		<td>Jan 12, 2024</td>
		
		<td><span>Processing</span></td>
	
	</tr>

  

<tr>
	
	<td>
	
		<b>Willem Dafoe</b> <br>
		
		Spider Inc
	
	</td>
	
	<td>ksh 30,000,000</td>
	
	<td>Feb 14, 2024</td>
	
	<td><span>Success</span></td>

</tr>

  

<tr>

	<td>
	
		<b>Chuck Norris</b> <br>
		
		Roundhouse Inc
	
	</td>
	
	<td>ksh 20,000,000</td>
	
	<td>March 14, 2024</td>
	
	<td><span>Success</span></td>

</tr>

  

<tr>

	<td>
	
		<b>Nick Cage</b> <br>
		
		Convicts Inc
	
	</td>
	
	<td>ksh 18,000,000</td>
	
	<td>April 14, 2024</td>
	
	<td><span>Reverted</span></td>

</tr>

  

</tbody>

  

<tfoot>
	
	<tr>
	
		<td>Total Paid</td>
		
		<td colspan="3">ksh 118,000,000</td>
	
	</tr>

</tfoot>

</table>
```