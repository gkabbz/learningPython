
# Convert date stored as string to date type
func = udf(lambda x: datetime.strptime(str(x), '%Y%m%d'), DateType())
cleanedCountryDatesUSRev = cleanedCountryUSRev.withColumn('date', func(col('submissionDateS3')))

installs = installs.withColumn('date', func(col('submission')))
installs = installs.withColumn('week', weekofyear(col('date')))
installs = installs.withColumn('year',