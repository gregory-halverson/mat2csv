library(R.matlab)

matlab.to.csv = function(matlab.filename, csv.filename, nodata.value)
{
  # Read .mat file
  data <- readMat(matlab.filename)
  data = data[[1]]
  
  # apply nodata value
  data[is.na(data) == TRUE] <- nodata.value
  
  # save table to csv
  write.table(data, csv.filename, col.names=FALSE, row.names=FALSE, sep=',')
}

args = commandArgs(trailingOnly=TRUE)
matlab.filename = args[1]
csv.filename = args[2]
nodata.value = args[3]

print(paste("matlab.filename: ", matlab.filename))
print(paste("csv.filename: ", csv.filename))
print(paste("nodata.value: ", nodata.value))

matlab.to.csv(matlab.filename, csv.filename, nodata.value)