suppressPackageStartupMessages(library(vecsets))
suppressPackageStartupMessages(library(ggplot2))

#' Add comma to thousands 
#'
#' @param amount, amount of money
#'
#' @return
#' @export
#'
#' @examples
format_number  <- function(amount) {
  format(round( as.numeric(amount)), big.mark = ",") 
}  

#' Get a new pack with m stickers with rare stickers
#'
#' @param collection, number of stickers to complete the album 
#' @param m, number of stickers per pack 
#' @param prob, vector with stickers probability distribution 
#'
#' @return
#' @export
#'
#' @examples
get_pack_new  <- function(collection, m, prob = NULL) {
  pack_new <- sample(collection, m, replace = FALSE, prob = prob)
}

#' Update the stickers swap stack
#'
#' @param album, album plus new package
#' @param pack_new, pack with new stickers
#' @param swap_stack, pool of duplicated stickers 
#'
#' @return
#' @export
#'
#' @examples
swap_stack_update  <-  function(album, pack_new, swap_stack) {
  album_tmp <- c(album, pack_new)
  idx <- duplicated(album_tmp)
  sticks <- unique(album_tmp[idx])
  swap_stack <- c(swap_stack, sticks)
  swap_stack
}

#' Update Panini album with new stickers
#'
#' @param album, album with unique stickers 
#' @param pack_new, pack with new stickers
#'
#' @return
#' @export
#'
#' @examples
album_update <-  function(album, pack_new) {
  album <- unique(c(album, pack_new))
}

#' Panini collector problem, Monte Carlo simulation for no-swapping strategy
#'
#' @param cs, vector with 1:CS stickers 
#' @param m, number of stickers per pack 
#'
#' @return
#' @export
#'
#' @examples
pcp_mc  <-  function(cs, m, prob = NULL) {
  
  album <- c()
  packs_bought <- 0
  collection <- 1:cs
  
  while (length(album) != length(collection)) {
    pack_new <- get_pack_new(collection, m, prob)
    album <- album_update(album, pack_new)
    packs_bought <- packs_bought + 1
  }
  packs_bought
}

#' Swap duplicated stickers among collectors, if available
#'
#' @param album_lst, list with collectors' albums
#' @param swap_stack_lst, list with collectors' swap stacks
#'
#' @return
#' @export
#'
#' @examples
swap_stickers <-  function(album_lst, swap_stack_lst) {
  N <- length(album_lst)
  # range for album loop
  # range_al <- 1:N
  range_rnd <- sample(1:N)
  range_ss <- range_rnd
  range_al <- range_rnd[-length(range_rnd)]
  for (i in range_al) {
    # range for swap stacks loop
    idx <- i == range_ss
    range_ss <- range_ss[!idx]
    for (j in range_ss) {
      # identify useful stickers in another collector's swap stacks
      idx <- swap_stack_lst[[j]] %in% album_lst[[i]]
      # identify useful stickers in my swap stacks
      jdx <- swap_stack_lst[[i]] %in% album_lst[[j]]
      # take useful stickers
      swap_j <- unique(swap_stack_lst[[j]][!idx])
      swap_i <- unique(swap_stack_lst[[i]][!jdx])
      # only the shortest swap stack can be swapped
      ni <- length(swap_i)
      nj <- length(swap_j)
      n <- min(c(ni, nj))
      # if at least one sticker can be swap...
      if (n > 0) {
        album_lst[[i]] <- album_update(album_lst[[i]], swap_j[1:n])
        album_lst[[j]] <- album_update(album_lst[[j]], swap_i[1:n])
        swap_stack_lst[[j]] <-
          vsetdiff(swap_stack_lst[[j]] , swap_j[1:n])
        swap_stack_lst[[i]] <-
          vsetdiff(swap_stack_lst[[i]] , swap_i[1:n])
      }
    }
  }
  r <- list(album_lst, swap_stack_lst)
  r
}

#' Panini collector problem, Monte Carlo simulation for swapping strategy
#'
#' @param cs, vector with 1:CS stickers 
#' @param m, number of stickers in a pack 
#' @param n, number of collectors
#' 
#' @return
#' @export
#'
#' @examples
pcp_swap_mc  <-  function(cs, m, n, prob = NULL) {
  album <- c()
  swap_stack <- c()
  packs_bought <- 0
  collection <- 1:cs
  
  collection_lst <- rep(list(collection), n)
  m_lst <- rep(list(m), n)
  album_lst <- rep(list(album), n)
  swap_stack_lst  <- rep(list(swap_stack), n)
  prob_lst  <- rep(list(prob), n)
  
  while (length(album_lst[[1]]) < cs) {
    pack_lst <- mapply(get_pack_new,
                       collection_lst,
                       m_lst, 
                       prob_lst, SIMPLIFY = FALSE)
    swap_stack_lst  <-  mapply(swap_stack_update,
                               album_lst,
                               pack_lst,
                               swap_stack_lst,
                               SIMPLIFY = FALSE)
    album_lst <- mapply(album_update,
                        album_lst,
                        pack_lst, SIMPLIFY = FALSE)
    
    r <- swap_stickers(album_lst, swap_stack_lst)
    album_lst <- r[[1]]
    swap_stack_lst <- r[[2]]
    
    packs_bought <- packs_bought + 1
  }
  packs_bought
}

#' Plot probability density
#'
#' @param cs, vector with 1:CS stickers
#' @param m, number of stickers in a pack
#'
#' @return
#' @export
#'
#' @examples
plot_density <- function(packs_needed) {
  packs_needed_m <- round(mean(packs_needed))
  
  q <- quantile(packs_needed, probs = seq(0, 1, 0.10))
  q_90 <- round(q[10])
  
  p <- ggplot(packs_needed %>% as.data.frame(),
              aes(x = (packs_needed))) +
    geom_histogram(aes(y = after_stat(count / max(count))), 
                   colour = "deepskyblue3", 
                   fill = "white"
                   ) +
    geom_density(aes(y = after_stat(count / max(count))), 
                alpha = .1, 
                 fill = "deepskyblue1"
                 # fill=if_else(x <= q_90,'deepskyblue1','white')
                 ) +
    geom_vline(
      aes(xintercept = packs_needed_m),
      linetype = "dashed",
      color = "deeppink",
      # color = "coral",
      size = 1
    ) +
    geom_vline(
      aes(xintercept = q[10]),
      linetype = "dashed",
      color = "deeppink",
      # color = "coral",
      size = 1
    ) +
    labs(x = "Number of packs" , y = "Density"
         ) +
    annotate(
      "text",
      x = packs_needed_m - packs_needed_m*0.075,
      y = -0.05,
      label = sprintf("mean=%g", packs_needed_m)
    ) +
    annotate(
      "text",
      x = q[10] + q[10]*0.075,
      y = -0.05,
      label = sprintf("90%%=%g", q_90)
    ) +
    theme_bw()
  p
}

#' Plot collectors vs. packs
#'
#' @param cs, vector with 1:CS stickers
#' @param m, number of stickers in a pack
#'
#' @return
#' @export
#'
#' @examples
plot_collectors_vs_packs <- function(range_n, packs_needed) {
  df <- data.frame(collectors = range_n,
                   packs_needed = packs_needed)
  
  
  p3 <- ggplot(df, aes(x = collectors, y = packs_needed)) +
    geom_line(color = "deepskyblue2",  size = 1) +
    geom_point(color = "deeppink", size = 2.5) +
    geom_segment(
      aes(
        x = 0,
        y = packs_needed,
        xend = collectors,
        yend = packs_needed,
      ),
      linetype = "dotted",
      color = "deeppink",
      size = 1
    ) +
    labs(x = "Collectors", y = "Packs needed") +
    theme_bw()
}
  