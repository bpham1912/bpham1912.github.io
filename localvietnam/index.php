<!doctype>
<html lang="en">
<head>
<link rel="stylesheet" type="text/css" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css">
<script type="text/javascript" charset="utf8" src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.js"></script>
<script src="https://code.jquery.com/jquery-3.5.1.min.js" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" crossorigin="anonymous"></script>

<script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
<script src="https://code.jquery.com/ui/1.12.1/jquery-ui.min.js" integrity="sha256-VazP97ZCwtekAsvgPBSUwPFKdrwD3unUfSGVYrahUqU=" crossorigin="anonymous"></script>
<script type="text/javascript"> 
	
$(document).ready(function() {
	$('#ss').DataTable();

    var table = $('#ss').DataTable({
        initComplete: function () {
            // Apply the search
            this.api().columns().every( function () {
                var that = this;
 
                $( 'input', this.footer() ).on( 'keyup change clear', function () {
                    if ( that.search() !== this.value ) {
                        that
                            .search( this.value )
                            .draw();
                    }
                } );
            } );
        }
    });
} );

</script>
</head>
<body>
<style>
thead input {
        width: 100%;
        padding: 3px;
        box-sizing: border-box;
    }
</style>
<div class="container" style="max-width:1000px;  display: block;
  margin-left: auto;
  margin-right: auto;">
<?php

require_once "Classes/PHPExcel.php";

		$tmpfname = "dvhcvn.xlsx";
		$excelReader = PHPExcel_IOFactory::createReaderForFile($tmpfname);
		$excelObj = $excelReader->load($tmpfname);
		$worksheet = $excelObj->getSheet(0);
		$lastRow = $worksheet->getHighestRow();
		
		echo "<table id='ss' class='display dataTable' role='grid' aria-describedby='empTable_info' style='width: 100%;'>";
		echo "<thead>
		<tr>
			<th>Tỉnh Thành Phố</th>
			
			<th>Huyện</th>
			
			<th>Xã/Thị trấn</th>
			
			<th>Loại</th>
		</tr>
	</thead>";
		echo " <tbody>";
	
		for ($row = 1; $row <= $lastRow; $row++) {
			 echo "<tr><td>";
			 echo $worksheet->getCell('A'.$row)->getValue();
			 echo "</td><td>";
			
			 echo $worksheet->getCell('C'.$row)->getValue();
			 echo "</td><td>";
			
			 echo $worksheet->getCell('E'.$row)->getValue();
			 echo "</td><td>";
			
			 echo $worksheet->getCell('G'.$row)->getValue();
			 echo "</td></tr>";
		}
		echo " </tbody>";
		echo "</table>";	
?>

</div>
</body>
</html>