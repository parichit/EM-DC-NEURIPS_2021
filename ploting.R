library(ggplot2)
library(gridExtra)
library(grid)

input_loc = file.path(trimws(getwd()), "benchmark_no_repeat_bkup")

# Set plot dimesions (inches)
fig_width = 16
fig_height = 14

# Load the data
read_data <- function(sub_folder, file_name){

  #print(file.path(sub_folder, paste(file_name , extension, sep="")))
  data <- read.csv2(file = file.path(sub_folder, file_name), sep = "\t",
                      header = FALSE,
                      stringsAsFactors = FALSE
  )

  data  = data[-1,]
  data =  apply(data, 2, as.numeric)
  return(data)
}


# Create data for bar plots
get_plot_matrix <- function(emdc_data, star_data, emt_data){

  emdc_data = rbind(emdc_data, star_data)
  emdc_data = rbind(emdc_data, emt_data)

  emdc_data = as.data.frame(emdc_data)
  emdc_data["Algorithm"] = c(rep("EMDC", 5), rep("EM*", 5), rep("EM-T", 5))

  colnames(emdc_data) <- c("Clusters", "ARI", "Accuracy", "Time", "Iterations", "Algorithm")

  emdc_data[, 1] = as.numeric(emdc_data[,1])
  emdc_data[, 2] = as.numeric(emdc_data[,2])
  emdc_data[, 3] = as.numeric(emdc_data[,3])
  emdc_data[, 4] = as.numeric(emdc_data[,4])
  emdc_data[, 5] = as.numeric(emdc_data[,5])

  return(emdc_data)
}

# size parameters
plot_title_size = 15
caption_size = 15
axis_label_size = 12
axis_tick_size= 10
legend_size = 12

# Color and font parameters
sub_plot_color = "dodgeblue"
font_color = "seagreen"

# Title and caption parameters
barplot_caption = "(A): Plots showing averaged results of 5 runs for training time, iterations and accuracy."

create_plot_for_clustering_data <-function(input_loc){

  print("Creating plot for clustering data.")

  # Set parameter values for number of cluster data
  plot_title = "Number of clusters experiment"
  file_name = "clustering_data"
  x_axis_label = "Number of clusters"

  # Read the data
  emdc_data = read_data(input_loc, "emdc_clustering_res.txt")
  star_data = read_data(input_loc, "emstar_clustering_res.txt")
  emt_data = read_data(input_loc, "emt_clustering_res.txt")

  # Get combined data
  combined_data = get_plot_matrix(emdc_data, star_data, emt_data)


  # Draw the bar plot
  p1 <- ggplot(data=combined_data, aes(x=Clusters, y=Time, fill=Algorithm)) + geom_bar(stat="identity", position=position_dodge(), aes(color=Algorithm), show.legend = FALSE)
  p1 <- p1 + labs(x = "Number of clusters", y = "Training time (seconds)") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0),
                                                                                                     colour = font_color),
                                                                           axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
                                                                           axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
                                                                           axis.text.x = element_text(face="bold", size = axis_tick_size),
                                                                           axis.text.y = element_text(face="bold", size = axis_tick_size),
                                                                           panel.background = element_rect(fill = "white"))


  p2 <- ggplot(data=combined_data, aes(x=Clusters, y=Iterations, fill=Algorithm)) +
    geom_bar(stat="identity", position=position_dodge(), aes(color=Algorithm), show.legend = FALSE)

  p2 <- p2 + labs(x = "Number of clusters", y = "Iterations")
  p2 <- p2 + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0)),
                    axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
                    axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
                    axis.text.x = element_text(face="bold", size = axis_tick_size),
                    axis.text.y = element_text(face="bold", size = axis_tick_size),
                    legend.title = element_text(face="bold", size=legend_size, color=font_color),
                    legend.text = element_text(face="bold", size = 15),
                    panel.background = element_rect(fill = "white"))


    p3 <- ggplot(data=combined_data, aes(x=Clusters, y=ARI, fill=Algorithm)) +
      geom_bar(stat="identity", position=position_dodge(), aes(color=Algorithm))

    p3 <- p3 + labs(x = "Number of clusters", y = "Adjusted Rand Index") +
            theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0)),
                                            axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
                                            axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
                                            axis.text.x = element_text(face="bold", size = axis_tick_size),
                                            axis.text.y = element_text(face="bold", size = axis_tick_size),
                                            panel.background = element_rect(fill = "white"))

  # # Combine the bar and box plots together
  num_cluster_plot = grid.arrange(p1, p2, p3, nrow=1, top=textGrob(plot_title, gp=gpar(fontface= "bold", fontsize=plot_title_size,
                                  col="firebrick3")), padding=unit(5, "line"))
  num_cluster_plot
  # # Save the plot on disk
  ggsave(file.path(input_loc, "plot_clustering.png"), num_cluster_plot,
  dpi=360, height=8, width=10, units="in")
}


create_plot_for_clustering_data(input_loc)

# create_plot_for_scalability_data <- function(input_loc){
#
#   print("Creating plot for scalability data.")
#
#   # Set parameter values for scalability data
#   plot_title = "Scalability experiment"
#   file_name = "scalability_data"
#   x_axis_label = "Number of data points (millions)"
#   axis_labels_vector = c("1", "1.5", "2", "2.5", "3")
#
#   # Read the data
#   star_time = read_data(input_loc, file_name, "_emstar_time.tsv")
#   star_iter = read_data(input_loc, file_name, "_emstar_iter.tsv")
#   emt_time = read_data(input_loc, file_name, "_emt_time.tsv")
#   emt_iter = read_data(input_loc, file_name, "_emt_iter.tsv")
#
#
#   # Get the data box plots results
#   time_plot = get_plot_matrix(star_time, emt_time)
#   iter_plot = get_plot_matrix(star_iter, emt_iter)
#
#   time_plot$Group <- factor(time_plot$Group, unique(time_plot$Group))
#   iter_plot$Group <- factor(iter_plot$Group, unique(iter_plot$Group))
#
#   # Draw the bar plot
#   p3 <- ggplot(data=time_plot, aes(x=Group, y=Values, fill=Implementation)) + geom_bar(stat="identity", width=0.5, position=position_dodge(),
#                                                                                        aes(color=Implementation), show.legend = FALSE)
#   p3 <- p3 + labs(x = x_axis_label, y = "Training time (seconds)") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0),
#                                                                                                      colour = font_color),
#                                                                            axis.title.x = element_text(face="bold", vjust=-0.5, size = axis_label_size),
#                                                                            axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
#                                                                            axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                            axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                            panel.background = element_rect(fill = "white"))+
#     scale_x_discrete(labels = axis_labels_vector)
#
#
#   # Draw the bar plotss
#   p4 <- ggplot(data=iter_plot, aes(x=Group, y=Values, fill=Implementation)) + geom_bar(stat="identity", width=0.5, position=position_dodge(),
#                                                                                        aes(color=Implementation))
#   p4 <- p4 + labs(x = x_axis_label, y = "Number of iterations") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size,
#                                                                                                   face="bold", margin = margin(10, 0, 10, 0),
#                                                                                                   colour = font_color),
#                                                                         axis.title.x = element_text(face="bold", vjust=-0.5, size = axis_label_size),
#                                                                         axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                         axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                         axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                         legend.title = element_text(face="bold", size=legend_size, color=font_color),
#                                                                         legend.text = element_text(face="bold", size = 20),
#                                                                         panel.background = element_rect(fill = "white"), legend.key.size = unit(2,"line"))+
#     scale_x_discrete(labels = axis_labels_vector)
#
#   scalability_plot = grid.arrange(p3, p4, nrow=1, top=textGrob(plot_title, gp=gpar(fontface= "bold", fontsize=plot_title_size,
#                                                                                    col="firebrick3")), padding=unit(5, "line"))
#   # Save the plot on disk
#   ggsave(file.path(input_loc, "plot_scalability.png"), scalability_plot, dpi=360, height=8,
#          width=10, units="in")
# }
#
#
# create_plot_for_dimensionality_data <- function(input_loc){
#
#   print("Creating plot for dimensionality data.")
#
#   # Set parameters for dimensionality data
#   plot_title = "Dimensionality experiment"
#   file_name= "dimensionality_data"
#   x_axis_label = "Number of dimensions"
#
#   # Read the data
#   star_time = read_data(input_loc, file_name, "_emstar_time.tsv")
#   star_iter = read_data(input_loc, file_name, "_emstar_iter.tsv")
#   emt_time = read_data(input_loc, file_name, "_emt_time.tsv")
#   emt_iter = read_data(input_loc, file_name, "_emt_iter.tsv")
#
#   time_avg_plot = get_avg_plot_matrix(star_time, emt_time)
#   iter_avg_plot = get_avg_plot_matrix(star_iter, emt_iter)
#
#   # Get the data box plots results
#   time_plot = get_plot_matrix(star_time, emt_time)
#   iter_plot = get_plot_matrix(star_iter, emt_iter)
#
#   time_avg_plot$Group <- factor(time_avg_plot$Group, unique(time_avg_plot$Group))
#   iter_avg_plot$Group <- factor(iter_avg_plot$Group, unique(iter_avg_plot$Group))
#
#   # Draw the bar plot
#   p5 <- ggplot(data=time_avg_plot, aes(x=Group, y=Avg, fill=Implementation)) + geom_bar(stat="identity", width = 0.6, position=position_dodge(), aes(color=Implementation), show.legend = FALSE)
#   p5 <- p5 + labs(x = x_axis_label, y = "Training time (seconds)") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0),
#                                                                                                      colour = font_color),
#                                                                            axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                            axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
#                                                                            axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                            axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                            panel.background = element_rect(fill = "white"))
#
#
#   # Draw the bar plot
#   p6 <- ggplot(data=iter_avg_plot, aes(x=Group, y=Avg, fill=Implementation)) + geom_bar(stat="identity", width = 0.6, position=position_dodge(), aes(color=Implementation))
#   p6 <- p6 + labs(title="EM-T failed to converge for d = 100 in multiple runs.", x = x_axis_label, y = "Number of iterations") + theme(plot.title = element_text(hjust = 0.5, size=axis_tick_size,
#                                                                                                                                                                  face="bold", margin = margin(10, 0, 10, 0), colour = font_color),
#                                                                                                                                        axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                                                                                        axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                                                                                        axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                                                                                        axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                                                                                        legend.title = element_text(face="bold", size=legend_size, color=font_color),
#                                                                                                                                        legend.text = element_text(face="bold", size = 20),
#                                                                                                                                        panel.background = element_rect(fill = "white"), legend.key.size = unit(2,"line"))
#
#   # Combine the bar and box plots together
#   dimensionality_plot = grid.arrange(p5, p6, nrow=1, top=textGrob(plot_title, gp=gpar(fontface= "bold", fontsize=plot_title_size,
#                                                                                       col="firebrick3")),padding=unit(5, "line"))
#
#   # Save the plot on disk
#   ggsave(file.path(input_loc, "plot_dimensionality.png"), dimensionality_plot, dpi=360, height=8,
#          width=10, units="in")
# }
#
#
# create_plot_for_synthetic_data <- function(){
#
#   print("Creating combined plot for synthetic datasets.")
#
#   # Create a vector to store the dataset name and plot title.
#   plot_data = c("num_cluster_analysis", "dims_analysis", "scal_analysis")
#   plot_data_title = c("Number of clusters experiments", "Dimensionality experiments", "Scalability experiments")
#
#   # Creae a data frame from the vectors
#   plot_frame = data.frame()
#   plot_frame = cbind(plot_data, plot_data_title)
#
#   # Set parameter values for number of cluster data
#   plot_title = "Number of clusters experiment"
#   file_name = "clustering_data"
#   x_axis_label = "Number of clusters"
#   sub_folder = file.path(input_data_loc, "simulated_datasets", "cluster_data")
#
#   # Read the data
#   star_time = read_data(sub_folder, file_name, "_emstar_time.tsv")
#   star_iter = read_data(sub_folder, file_name, "_emstar_iter.tsv")
#   emt_time = read_data(sub_folder, file_name, "_emt_time.tsv")
#   emt_iter = read_data(sub_folder, file_name, "_emt_iter.tsv")
#
#   time_avg_plot = get_avg_plot_matrix(star_time, emt_time)
#   iter_avg_plot = get_avg_plot_matrix(star_iter, emt_iter)
#
#   # Get the data box plots results
#   time_plot = get_plot_matrix(star_time, emt_time)
#   iter_plot = get_plot_matrix(star_iter, emt_iter)
#
#   time_avg_plot$Group <- factor(time_avg_plot$Group, unique(time_avg_plot$Group))
#   iter_avg_plot$Group <- factor(iter_avg_plot$Group, unique(iter_avg_plot$Group))
#
#   # Draw the bar plot
#   p1 <- ggplot(data=time_avg_plot, aes(x=Group, y=Avg, fill=Implementation)) + geom_bar(stat="identity", width=0.6, position=position_dodge(), aes(color=Implementation), show.legend = FALSE)
#   p1 <- p1 + labs(x = x_axis_label, y = "Training time (seconds)") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0),
#                                                                                                      colour = font_color),
#                                                                            axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                            axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
#                                                                            axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                            axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                            panel.background = element_rect(fill = "white"))
#
#
#   # Draw the bar plot
#   p2 <- ggplot(data=iter_avg_plot, aes(x=Group, y=Avg, fill=Implementation)) + geom_bar(stat="identity", width=0.6, position=position_dodge(), aes(color=Implementation))
#   p2 <- p2 + labs(title="EM-T failed to converge for all values of k in multiple runs.", x = x_axis_label, y = "Number of iterations") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0),
#                                                                                                                                                                          colour = font_color),
#                                                                                                                                                axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                                                                                                axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                                                                                                axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                                                                                                axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                                                                                                legend.title = element_text(face="bold", size=legend_size, color=font_color),
#                                                                                                                                                legend.text = element_text(face="bold", size = 20),
#                                                                                                                                                panel.background = element_rect(fill = "white"), legend.key.size = unit(2,"line"))
#
#   # Combine the bar and box plots together
#   num_cluster_plot = grid.arrange(p1, p2, nrow=1, top=textGrob(plot_title, gp=gpar(fontface= "bold", fontsize=plot_title_size,
#                                                                                    col="firebrick3")), padding=unit(5, "line"))
#
#
#   # Set parameter values for scalability data
#   plot_title = "Scalability experiment"
#   file_name = "scalability_data"
#   x_axis_label = "Number of data points (millions)"
#   axis_labels_vector = c("1", "1.5", "2", "2.5", "3")
#   sub_folder = file.path(input_data_loc, "simulated_datasets", "scalability_data/")
#
#   # Read the data
#   star_time = read_data(sub_folder, file_name, "_emstar_time.tsv")
#   star_iter = read_data(sub_folder, file_name, "_emstar_iter.tsv")
#   emt_time = read_data(sub_folder, file_name, "_emt_time.tsv")
#   emt_iter = read_data(sub_folder, file_name, "_emt_iter.tsv")
#
#
#   # Get the data box plots results
#   time_plot = get_plot_matrix(star_time, emt_time)
#   iter_plot = get_plot_matrix(star_iter, emt_iter)
#
#   time_plot$Group <- factor(time_plot$Group, unique(time_plot$Group))
#   iter_plot$Group <- factor(iter_plot$Group, unique(iter_plot$Group))
#
#   # Draw the bar plot
#   p3 <- ggplot(data=time_plot, aes(x=Group, y=Values, fill=Implementation)) + geom_bar(stat="identity", width=0.5, position=position_dodge(),
#                                                                                        aes(color=Implementation), show.legend = FALSE)
#   p3 <- p3 + labs(x = x_axis_label, y = "Training time (seconds)") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0),
#                                                                                                      colour = font_color),
#                                                                            axis.title.x = element_text(face="bold", vjust=-0.5, size = axis_label_size),
#                                                                            axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
#                                                                            axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                            axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                            panel.background = element_rect(fill = "white"))+
#     scale_x_discrete(labels = axis_labels_vector)
#
#
#   # Draw the bar plotss
#   p4 <- ggplot(data=iter_plot, aes(x=Group, y=Values, fill=Implementation)) + geom_bar(stat="identity", width=0.5, position=position_dodge(),
#                                                                                        aes(color=Implementation))
#   p4 <- p4 + labs(x = x_axis_label, y = "Number of iterations") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size,
#                                                                                                   face="bold", margin = margin(10, 0, 10, 0),
#                                                                                                   colour = font_color),
#                                                                         axis.title.x = element_text(face="bold", vjust=-0.5, size = axis_label_size),
#                                                                         axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                         axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                         axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                         legend.title = element_text(face="bold", size=legend_size, color=font_color),
#                                                                         legend.text = element_text(face="bold", size = 20),
#                                                                         panel.background = element_rect(fill = "white"), legend.key.size = unit(2,"line"))+
#     scale_x_discrete(labels = axis_labels_vector)
#
#   scalability_plot = grid.arrange(p3, p4, nrow=1, top=textGrob(plot_title, gp=gpar(fontface= "bold", fontsize=plot_title_size,
#                                                                                    col="firebrick3")), padding=unit(5, "line"))
#
#
#   # # Set parameters for dimensionality data
#   plot_title = "Dimensionality experiment"
#   file_name= "dimensionality_data"
#   x_axis_label = "Number of dimensions"
#   sub_folder = file.path(input_data_loc, "simulated_datasets", "dimensionality_data")
#
#   # Read the data
#   star_time = read_data(sub_folder, file_name, "_emstar_time.tsv")
#   star_iter = read_data(sub_folder, file_name, "_emstar_iter.tsv")
#   emt_time = read_data(sub_folder, file_name, "_emt_time.tsv")
#   emt_iter = read_data(sub_folder, file_name, "_emt_iter.tsv")
#
#   time_avg_plot = get_avg_plot_matrix(star_time, emt_time)
#   iter_avg_plot = get_avg_plot_matrix(star_iter, emt_iter)
#
#   # Get the data box plots results
#   time_plot = get_plot_matrix(star_time, emt_time)
#   iter_plot = get_plot_matrix(star_iter, emt_iter)
#
#   time_avg_plot$Group <- factor(time_avg_plot$Group, unique(time_avg_plot$Group))
#   iter_avg_plot$Group <- factor(iter_avg_plot$Group, unique(iter_avg_plot$Group))
#
#   # Draw the bar plot
#   p5 <- ggplot(data=time_avg_plot, aes(x=Group, y=Avg, fill=Implementation)) + geom_bar(stat="identity", width = 0.6, position=position_dodge(), aes(color=Implementation), show.legend = FALSE)
#   p5 <- p5 + labs(x = x_axis_label, y = "Training time (seconds)") + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0),
#                                                                                                      colour = font_color),
#                                                                            axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                            axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
#                                                                            axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                            axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                            panel.background = element_rect(fill = "white"))
#
#
#   # Draw the bar plot
#   p6 <- ggplot(data=iter_avg_plot, aes(x=Group, y=Avg, fill=Implementation)) + geom_bar(stat="identity", width = 0.6, position=position_dodge(), aes(color=Implementation))
#   p6 <- p6 + labs(title="EM-T failed to converge for d = 100 in multiple runs.", x = x_axis_label, y = "Number of iterations") + theme(plot.title = element_text(hjust = 0.5, size=axis_tick_size,
#                                                                                                                                                                  face="bold", margin = margin(10, 0, 10, 0), colour = font_color),
#                                                                                                                                        axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                                                                                        axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
#                                                                                                                                        axis.text.x = element_text(face="bold", size = axis_tick_size),
#                                                                                                                                        axis.text.y = element_text(face="bold", size = axis_tick_size),
#                                                                                                                                        legend.title = element_text(face="bold", size=legend_size, color=font_color),
#                                                                                                                                        legend.text = element_text(face="bold", size = 20),
#                                                                                                                                        panel.background = element_rect(fill = "white"), legend.key.size = unit(2,"line"))
#
#   # Combine the bar and box plots together
#   dimensionality_plot = grid.arrange(p5, p6, nrow=1, top=textGrob(plot_title, gp=gpar(fontface= "bold", fontsize=plot_title_size,
#                                                                                       col="firebrick3")),padding=unit(5, "line"))
#
#
#   # Combine all plots together
#   final_plot = grid.arrange(num_cluster_plot, scalability_plot, dimensionality_plot, nrow=3)
#
#   # Save the plot on disk
#   ggsave(file.path(input_data_loc, "Figure-9.png"), final_plot, dpi=360, height=32,
#          width=30, units="in")
# }
#
#
#
# create_plot_for_real_data <- function(plot_data, plot_data_title, output_dir, out_name){
#
#   # reset size parameters (for small graph)
#   plot_title_size = 20
#   caption_size = 18
#   axis_label_size = 17
#   axis_tick_size= 17
#   legend_size = 15
#
#   # Creae a data frame from the vectors
#   plot_frame = data.frame()
#   plot_frame = cbind(plot_data, plot_data_title)
#
#   # Call the function in a loop to create plots for all datasets
#   for (i in 1:nrow(plot_frame)){
#
#     file_name = plot_frame[i, 1]
#     plot_title = plot_frame[i, 2]
#     x_axis_label = "Number of clusters"
#     sub_folder = file.path(input_data_loc, "real_datasets")
#
#     print(paste("Creating plots for: ", plot_title))
#
#     # Read the data
#     star_time = read_data(output_dir, file_name, "_emstar_time.tsv")
#     star_iter = read_data(output_dir, file_name, "_emstar_iter.tsv")
#     star_acc = read_data(output_dir, file_name, "_emstar_acc.tsv")
#     emt_time = read_data(output_dir, file_name, "_emt_time.tsv")
#     emt_iter = read_data(output_dir, file_name, "_emt_iter.tsv")
#     emt_acc = read_data(output_dir, file_name, "_emt_acc.tsv")
#     output_loc = output_dir
#
#     time_avg_plot = get_avg_plot_matrix(star_time, emt_time)
#     iter_avg_plot = get_avg_plot_matrix(star_iter, emt_iter)
#     acc_avg_plot = get_avg_plot_matrix(star_acc, emt_acc)
#
#     # Get the data box plots results
#     time_plot = get_plot_matrix(star_time, emt_time)
#     iter_plot = get_plot_matrix(star_iter, emt_iter)
#     acc_plot = get_plot_matrix(star_acc, emt_acc)
#
#     # Call the function to create plots
#     create_plots_real_data(
#       time_avg_plot,
#       iter_avg_plot,
#       acc_avg_plot,
#       time_plot,
#       iter_plot,
#       acc_plot,
#       plot_title,
#       x_axis_label,
#       barplot_caption,
#       boxplot_caption,
#       plot_title_size,
#       caption_size,
#       legend_size,
#       axis_label_size,
#       axis_tick_size,
#       font_family,
#       font_color,
#       output_dir,
#       out_name
#     )
#   }
#
# }
#
