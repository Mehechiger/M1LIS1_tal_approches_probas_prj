library(hash)

input<-"/Users/mehec/nlp/approbas/prj/scores/"
output<-"/Users/mehec/nlp/approbas/prj/plots/is_norm/"
list_data<-list("da","bleu","terp")

dir.create(output)

res=hash()

for (data in list_data){
	assign(data, read.delim(paste(input, data, "..seg.scr", sep=""), header=FALSE)[,-2])

	list_direction<-unique(get(data)$V1)
	for (direction in list_direction){
		data_direction = paste(data, direction , sep="_")

		assign(data_direction, get(data)[which(get(data)$V1==direction), c("V1","V3","V4","V5")])

		png(paste(output,data_direction, "hist.jpg", sep="_"))
		plot(hist(get(data_direction)$V5), main=paste("hist",data_direction))
		dev.off()

		png(paste(output,data_direction, "qqnorm.jpg", sep="_"))
		plot(qqnorm(get(data_direction)$V5), main=paste("qqnorm", data_direction))
		#plot(qqline(get(data_direction)$V5))
		dev.off()

		.set(res, keys=data_direction, values=shapiro.test(get(data_direction)$V5)$p.value>0.05)

		list_langpair<-unique(get(data)$V3)
		for (lang_pair in list_langpair){
			data_direction_langpair=paste(data_direction, lang_pair, sep="_")

			assign(data_direction_langpair, get(data_direction)[which(get(data_direction)$V3==lang_pair), c("V1","V3","V4","V5")])

			png(paste(output, data_direction_langpair,"hist.jpg",sep="_"))
			plot(hist(get(data_direction_langpair)$V5), main=paste("hist",data_direction_langpair))
			dev.off()

			png(paste(output, data_direction_langpair,"qqnorm.jpg", sep="_"))
			plot(qqnorm(get(data_direction_langpair)$V5), main=paste("qqnorm", data_direction_langpair))
			#plot(qqline(get(data_direction_langpair)$V5))
			dev.off()

			.set(res, keys=data_direction_langpair, values=shapiro.test(get(data_direction_langpair)$V5)$p.value>0.05)
		}
	}
}

write.table(res, file=paste(output, is_norm.csv, sep=""))
