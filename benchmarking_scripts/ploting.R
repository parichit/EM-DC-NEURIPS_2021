# Parichit Sharma, Department of Computer Science, IUB
# A visualization script to create the comparative bar plots for
# the output data.

library(ggplot2)
library(gridExtra)
library(grid)


input_loc = file.path(dirname(trimws(getwd())))

# Set plot dimesions (inches)
fig_width = 12
fig_height = 6

# Load the data
read_data <- function(file_path){

  #print(file.path(sub_folder, paste(file_name , extension, sep="")))
  data <- read.csv2(file = file_path, sep = "\t", header = FALSE, stringsAsFactors = FALSE)

  data  = data[-1,]
  data =  apply(data, 2, as.numeric)
  return(data)
}


# Create data for bar plots
get_plot_matrix <- function(emdc_data, star_data, emt_data, key){

  emdc_data = rbind(emdc_data, star_data)
  emdc_data = rbind(emdc_data, emt_data)

  emdc_data = as.data.frame(emdc_data)
  emdc_data["Algorithm"] = c(rep("EMDC", 5), rep("EM*", 5), rep("EM-T", 5))

  colnames(emdc_data) <- c(key, "ARI", "Accuracy", "Time", "Iterations", "Algorithm")

  emdc_data[, 1] = as.numeric(emdc_data[,1])
  emdc_data[, 2] = as.numeric(emdc_data[,2])
  emdc_data[, 3] = as.numeric(emdc_data[,3])
  emdc_data[, 4] = as.numeric(emdc_data[,4])
  emdc_data[, 5] = as.numeric(emdc_data[,5])

  return(emdc_data)
}


# size parameters
plot_title_size = 25
axis_label_size = 20
axis_tick_size= 18
font_color = "#D55E00"

cbPalette <- c("#999999", "#E69F00", "#56B4E9", "#009E73", "#F0E442", "#0072B2", "#D55E00", "#CC79A7")

create_plot <-function(input_loc){

  print("Creating plot for clustering data.")

  # Set parameter values for number of cluster data
  plot_title = "Clustering experiment (Dimensions: 10, Data size: 321093)"
  file_name = "clustering_data"
  x_axis_label = "Number of clusters"

  # Read the data
  emdc_data = read_data(file.path(input_loc, "benchmark_clus", "emdc_res.txt"))
  star_data = read_data(file.path(input_loc, "benchmark_clus", "emstar_res.txt"))
  emt_data = read_data(file.path(input_loc, "benchmark_clus", "emt_res.txt"))

  # Get combined data
  combined_data = get_plot_matrix(emdc_data, star_data, emt_data, "Clusters")


  # Draw the bar plot
  p1 <- ggplot(data=combined_data, aes(x=factor(Clusters), y=Time, fill=Algorithm)) + 
    geom_bar(stat="identity", position=position_dodge(), show.legend = FALSE)
  p1 <- p1 + labs(x = "Number of clusters", y = "Training time (seconds)") + 
    theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", 
          margin = margin(10, 0, 10, 0), colour = font_color),
    axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
    axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
    axis.text.x = element_text(face="bold", size = axis_tick_size),
    axis.text.y = element_text(face="bold", size = axis_tick_size),
    panel.background = element_rect(fill = "white"))
  
  p1 <- p1 + scale_fill_manual(values = cbPalette)


  p2 <- ggplot(data=combined_data, aes(x=factor(Clusters), y=Iterations, fill=Algorithm)) +
    geom_bar(stat="identity", position=position_dodge(), show.legend = TRUE)

  p2 <- p2 + labs(x = "Number of clusters", y = "Iterations")
  p2 <- p2 + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0)),
                    axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
                    axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
                    axis.text.x = element_text(face="bold", size = axis_tick_size),
                    axis.text.y = element_text(face="bold", size = axis_tick_size),
                    legend.position = "top",
                    legend.title = element_text(face="bold", size=18),
                    legend.text = element_text(face="bold", size = 15),
                    panel.background = element_rect(fill = "white"))

  p2 <- p2 + scale_fill_manual(values = cbPalette)
  
  legend <- get_legend(p2)
  

    p3 <- ggplot(data=combined_data, aes(x=factor(Clusters), y=ARI, fill=Algorithm)) +
      geom_bar(stat="identity", position=position_dodge(), show.legend = FALSE)

    p3 <- p3 + labs(x = "Number of clusters", y = "Adjusted Rand Index") +
            theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0)),
                                            axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
                                            axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
                                            axis.text.x = element_text(face="bold", size = axis_tick_size),
                                            axis.text.y = element_text(face="bold", size = axis_tick_size),
                                            panel.background = element_rect(fill = "white"))

    p3 <- p3 + scale_fill_manual(values = cbPalette)
  
  # Combine the bar and box plots together
  clus_plot = grid.arrange(p1, p2, p3, nrow=1,
                                  top=textGrob(plot_title,
                                  gp=gpar(fontface= "bold", fontsize=plot_title_size,
                                  col=font_color)), padding=unit(5, "line"))
  
  
  print("#####################################")
  print("Creating plot for dimensionality data.")
  print("#####################################")
  
  # Set parameters for dimensionality data
  plot_title = "Dimensionality experiment (Number of clusters: 10, Data size: 321093)"
  file_name= "dimensionality_data"
  x_axis_label = "Number of dimensions"
  
  # Read the data
  emdc_data = read_data(file.path(input_loc, "benchmark_dims", "emdc_res.txt"))
  star_data = read_data(file.path(input_loc, "benchmark_dims", "emstar_res.txt"))
  emt_data = read_data(file.path(input_loc, "benchmark_dims", "emt_res.txt"))
  
  # Get combined data
  combined_data = get_plot_matrix(emdc_data, star_data, emt_data, "Dimensions")
  
  
  # Draw the bar plot
  p1 <- ggplot(data=combined_data, aes(x=factor(Dimensions), y=Time, fill=Algorithm)) + 
    geom_bar(stat="identity", position=position_dodge(), show.legend = FALSE)
  p1 <- p1 + labs(x = "Dimensions", y = "Training time (seconds)") + 
    theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", 
                                    margin = margin(10, 0, 10, 0), colour = font_color),
          axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
          axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
          axis.text.x = element_text(face="bold", size = axis_tick_size),
          axis.text.y = element_text(face="bold", size = axis_tick_size),
          panel.background = element_rect(fill = "white"))
  p1 <- p1 + scale_fill_manual(values = cbPalette)
  
  
  p2 <- ggplot(data=combined_data, aes(x=factor(Dimensions), y=Iterations, fill=Algorithm)) +
    geom_bar(stat="identity", position=position_dodge(), show.legend = FALSE)
  
  p2 <- p2 + labs(x = "Dimensions", y = "Iterations")
  p2 <- p2 + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0)),
                   axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
                   axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
                   axis.text.x = element_text(face="bold", size = axis_tick_size),
                   axis.text.y = element_text(face="bold", size = axis_tick_size),
                   panel.background = element_rect(fill = "white"))
  
  p2 <- p2 + scale_fill_manual(values = cbPalette)
  
  
  p3 <- ggplot(data=combined_data, aes(x=factor(Dimensions), y=ARI, fill=Algorithm)) +
    geom_bar(stat="identity", position=position_dodge(), show.legend = FALSE)
  
  p3 <- p3 + labs(x = "Dimensions", y = "Adjusted Rand Index") +
    theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0)),
          axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
          axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
          axis.text.x = element_text(face="bold", size = axis_tick_size),
          axis.text.y = element_text(face="bold", size = axis_tick_size),
          panel.background = element_rect(fill = "white"))
  
  p3 <- p3 + scale_fill_manual(values = cbPalette)
  
  # # Combine the bar and box plots together
  dims_plot = grid.arrange(p1, p2, p3, nrow=1,
                               top=textGrob(plot_title,
                                            gp=gpar(fontface= "bold", fontsize=plot_title_size,
                                                    col=font_color)), padding=unit(5, "line"))
  
  
  print("#####################################")
  print("Creating plot for Scalability data.")
  print("#####################################")
  
  plot_title = "Scalability experiment (Number of clusters:10, Dimensions: 30)"
  x_axis_label = "Number of data points (thousands)"

  # Read the data
  emdc_data = read_data(file.path(input_loc, "benchmark_scal", "emdc_res.txt"))
  star_data = read_data(file.path(input_loc, "benchmark_scal", "emstar_res.txt"))
  emt_data = read_data(file.path(input_loc, "benchmark_scal", "emt_res.txt"))

  # Get combined data
  combined_data = get_plot_matrix(emdc_data, star_data, emt_data, "Num_points")

  # Draw the bar plot
  p1 <- ggplot(data=combined_data, aes(x=factor(Num_points), y=Time, fill=Algorithm)) +
    geom_bar(stat="identity", position=position_dodge(), show.legend = FALSE)
  p1 <- p1 + labs(x = "Data size (thousands)", y = "Training time (seconds)") +
    theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold",
                                    margin = margin(10, 0, 10, 0), colour = font_color),
          axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
          axis.title.y = element_text(face="bold", hjust=0.5, size = axis_label_size),
          axis.text.x = element_text(face="bold", size = axis_tick_size),
          axis.text.y = element_text(face="bold", size = axis_tick_size),
          panel.background = element_rect(fill = "white"))
  p1 <- p1 + scale_fill_manual(values = cbPalette)


  p2 <- ggplot(data=combined_data, aes(x=factor(Num_points), y=Iterations, fill=Algorithm)) +
    geom_bar(stat="identity", position=position_dodge(), show.legend = FALSE)

  p2 <- p2 + labs(x = "Data size (thousands)", y = "Iterations")
  p2 <- p2 + theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0)),
                   axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
                   axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
                   axis.text.x = element_text(face="bold", size = axis_tick_size),
                   axis.text.y = element_text(face="bold", size = axis_tick_size),
                   panel.background = element_rect(fill = "white"))

  p2 <- p2 + scale_fill_manual(values = cbPalette)


  p3 <- ggplot(data=combined_data, aes(x=factor(Num_points), y=ARI, fill=Algorithm)) +
    geom_bar(stat="identity", position=position_dodge(), show.legend = FALSE)

  p3 <- p3 + labs(x = "Data size (thousands)", y = "Adjusted Rand Index") +
    theme(plot.title = element_text(hjust = 0.5, size=axis_label_size, face="bold", margin = margin(10, 0, 10, 0)),
          axis.title.x = element_text(face="bold", vjust=0.5, size = axis_label_size),
          axis.title.y = element_text(face="bold", vjust=0.5, size = axis_label_size),
          axis.text.x = element_text(face="bold", size = axis_tick_size),
          axis.text.y = element_text(face="bold", size = axis_tick_size),
          panel.background = element_rect(fill = "white"))

  p3 <- p3 + scale_fill_manual(values = cbPalette)

  # # Combine the bar and box plots together
  scal_plot = grid.arrange(p1, p2, p3, nrow=1,
                               top=textGrob(plot_title,
                                            gp=gpar(fontface= "bold", fontsize=plot_title_size,
                                                    col=font_color)), padding=unit(5, "line"))

  
  # Combine all plots together
  # final_plot = grid.arrange(clus_plot, dims_plot, nrow=2)
  final_plot = grid.arrange(clus_plot, dims_plot, scal_plot, nrow=3)
  
  # Save the plot on disk
  ggsave(file.path(input_loc, "Figure-1.png"), final_plot, dpi=360, height=18,
         width=15, units="in")
}


create_plot(input_loc)





